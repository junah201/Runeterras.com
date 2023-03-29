import requests
import os
import models
import database
from datetime import datetime
from typing import Dict
import boto3
from sqlalchemy import literal
from sqlalchemy.sql import exists

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")
DISCORD_WEBHOOKS_CHECK_NEW_PLAYER_LOG = os.environ.get(
    "DISCORD_WEBHOOKS_CHECK_NEW_PLAYER_LOG")


def check_new_player() -> Dict:
    log = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total received": 0,
        "new players": [],
        "updated players": [],
        "rate limit": False,
        "error": "",
        "end": None,
    }

    sqs_client = boto3.resource('sqs', region_name='ap-northeast-2')
    new_player_puuid_sqs = sqs_client.get_queue_by_name(
        QueueName='LOR__new-palyer-puuid-queue')

    db = next(database.get_db())

    for _ in range(100):
        new_players = new_player_puuid_sqs.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )

        if not new_players:
            break

        log["total received"] += len(new_players)

        for new_player in new_players:
            new_player_puuid, last_match_id, last_matched_at = map(
                str,
                new_player.body.split("\n")
            )

            # 이미 DB에 수집된 puuid인지 확인
            is_collected: bool = db.query(literal(True)).filter(db.query(models.Player).filter(
                models.Player.puuid == new_player_puuid
            ).exists()).scalar()
            if is_collected == True:
                print("already collected")
                new_player.delete()
                continue

            account_res = requests.get(
                f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/{new_player_puuid}",
                headers={
                    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Riot-Token": RIOT_API_KEY,
                },
                timeout=1
            )

            if account_res.status_code == 429:
                print("Rate limit")
                log["rate limit"] = True
                return log

            new_player.delete()

            if account_res.status_code != 200:
                print(account_res.text)
                log["error"] += account_res.text + "\n"
                continue

            account_data = account_res.json()

            db_new_player: models.Player = db.query(models.Player).filter(
                models.Player.game_name == account_data["gameName"], models.Player.puuid == None).first()

            if db_new_player:
                print("update", db_new_player.game_name, new_player_puuid)
                log["updated players"].append(
                    f"{db_new_player.game_name}\n")

                db_new_player.puuid = new_player_puuid
                db_new_player.game_name = account_data["gameName"]
                db_new_player.tag_line = account_data["tagLine"]
                db_new_player.last_matched_game_id = last_match_id
                db_new_player.last_matched_at = last_matched_at

                db.commit()
                continue

            print("new", account_data["gameName"], new_player_puuid)
            log["new players"].append(
                f"{account_data['gameName']}\n")
            db_new_player = models.Player(
                puuid=new_player_puuid,
                game_name=account_data["gameName"],
                tag_line=account_data["tagLine"],
                last_matched_game_id=last_match_id,
                last_matched_at=last_matched_at,
                is_master=False
            )
            db.add(db_new_player)
            db.commit()

    return log


def lambda_handler(event, context):
    log = check_new_player()
    log["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    success_color = 0x2ECC71
    error_color = 0xE74C3C

    if log["rate limit"] or log["error"]:
        color = error_color
    else:
        color = success_color

    data = {
        "content": "",
        "embeds": [
            {
                "title": "신규 유저 수집 로그",
                "description": f"""
                총 `{log["total received"]}`개의 puuid를 받았습니다.

                새로운 유저 : `{len(log["new players"])}`명
                {"```" + "".join([f"{player}" for player in log["new players"]]) + "```" if log["new players"] else ""}

                기존 마스터 유저 : `{len(log["updated players"])}`명
                {"```" + "".join([f"{player}" for player in log["updated players"]]) + "```" if log["updated players"] else ""}

                error : {"```" + "".join([f"{error}" for error in log["error"]]) + "```" if log["error"] else ""}
                rate limit : `{log["rate limit"]}`

                시작 : `{log["start"]}`
                종료 : `{log["end"]}`
                """,
                "color": color,
                "footer": {
                    "text": str(log["start"])
                }
            }
        ]
    }

    requests.post(
        DISCORD_WEBHOOKS_CHECK_NEW_PLAYER_LOG,
        json=data
    )

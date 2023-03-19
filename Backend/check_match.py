import requests
import os
import models
import database
from datetime import datetime
from typing import Tuple, Dict, Optional, List
import boto3

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")
DISCORD_WEBHOOKS_CHECK_MATCH_LOG = os.environ.get(
    "DISCORD_WEBHOOKS_CHECK_MATCH_LOG")

header_row = [
    "data_version",
    "match_id",
    "game_mode",
    "game_type",
    "game_start_time_utc",
    "game_version",
    "win_user_puuid",
    "win_user_deck_id",
    "win_user_deck_code",
    "win_user_order_of_play",
    "loss_user_puuid",
    "loss_user_deck_id",
    "loss_user_deck_code",
    "loss_user_order_of_play",
    "total_turn_count",
]


def check_match() -> Dict:
    log = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total checked": 0,
        "new ranked matches": 0,
        "end": None,
        "rate limit": False,
    }

    db = database.get_db()

    db_master_players_puuid: List[models.Player] = db.query(models.Player) \
        .filter(models.Player.is_master == True, models.Player.puuid != None) \
        .order_by(models.Player.last_checked_at.asc(), models.Player.last_matched_at.desc()).all()

    new_match_ids = []

    for db_master_player in db_master_players_puuid:
        print("start", db_master_player.puuid)
        res = requests.get(
            f"https://apac.api.riotgames.com/lor/match/v1/matches/by-puuid/{db_master_player.puuid}/ids",
            headers={
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Riot-Token": RIOT_API_KEY,
            },
            timeout=3
        )

        if res.status_code != 200:
            print(res.text)
            if res.status_code == 429:
                print("Too many requests")
                log["rate limit"] = True
                break
            continue

        log["total checked"] += 1

        match_ids = res.json()

        new_last_match_id: Optional[str] = None
        if match_ids:
            new_last_match_id = match_ids[0]

        for match_id in match_ids:
            if match_id == db_master_player.last_matched_game_id:
                print("Already checked")
                break

            print("match_id", match_id)
            new_match_ids.append(match_id)

        db_master_player.last_matched_game_id = new_last_match_id
        db_master_player.last_checked_at = datetime.utcnow()
        db.commit()
        print("end", db_master_player.puuid)

    log["new ranked matches"] = len(new_match_ids)

    sqs_client = boto3.resource('sqs', region_name='ap-northeast-2')
    match_id_sqs = sqs_client.get_queue_by_name(
        QueueName='LOR__match-data-queue.fifo')

    for idx in range(0, len(new_match_ids), 10):
        match_id_sqs.send_messages(
            Entries=[
                {
                    "Id": match_id,
                    "MessageBody": match_id,
                } for match_id in new_match_ids[idx:idx+10]
            ]
        )

    db.commit()
    return log


def lambda_handler(event, context):
    log = check_match()
    log["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    success_color = 0x2ECC71
    error_color = 0xE74C3C

    if log["rate limit"]:
        color = error_color
    else:
        color = success_color

    data = {
        "content": "",
        "embeds": [
            {
                "title": "매치 수집 로그",
                "description": f"""
                총 `{log["total checked"]}`명의 마스터 플레이어의 매치를 수집했습니다.

                새로운 랭크 매치 `{log["new ranked matches"]}`개를 발견했습니다.

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
        DISCORD_WEBHOOKS_CHECK_MATCH_LOG,
        json=data
    )

    return log

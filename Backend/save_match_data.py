import requests
import os
import models
import database
from datetime import datetime
import gzip
from typing import Tuple, Dict, Optional, List
import boto3
import uuid

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")
DISCORD_WEBHOOKS_CHECK_MATCH_LOG = os.environ.get(
    "DISCORD_WEBHOOKS_CHECK_MATCH_LOG")
TEST_MATCH_ID = os.environ.get("TEST_MATCH_ID")

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


def get_match_data_datail() -> Tuple[List, Dict]:
    log = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total receive data count": 0,
        "total save data count": 0,
        "end": None,
        "error": "",
        "rate limit": False,
    }
    match_datas = []

    db = database.get_db()

    init_res = requests.get(
        f"https://apac.api.riotgames.com/lor/match/v1/matches/{TEST_MATCH_ID}",
        headers={
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": RIOT_API_KEY,
        },
        timeout=3
    )

    # rate limit
    if init_res.status_code == 429:
        log["rate limit"] = True
        return match_datas, log

    # error
    if init_res.status_code != 200:
        log["error"] = init_res.text
        return match_datas, log

    max_number = int(init_res.headers["X-Method-Rate-Limit"].split(":")[0]) - int(
        init_res.headers["X-Method-Rate-Limit-Count"].split(":")[0])

    sqs_client = boto3.resource('sqs', region_name='ap-northeast-2')
    match_id_sqs = sqs_client.get_queue_by_name(
        QueueName='LOR__match-data-queue')
    new_player_puuid_sqs = sqs_client.get_queue_by_name(
        QueueName='LOR__new-palyer-puuid-queue')

    for _ in range(0, max_number, 10):
        match_ids = match_id_sqs.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )

        if not match_ids:
            break

        log["total receive data count"] += len(match_ids)

        for match_id in match_ids:
            print("match id", match_id.body)

            match_res = requests.get(
                f"https://apac.api.riotgames.com/lor/match/v1/matches/{match_id.body}",
                headers={
                    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Riot-Token": RIOT_API_KEY,
                },
                timeout=1
            )

            # rate limit
            if match_res.status_code == 429:
                print("rate limit")
                log["rate limit"] = True
                break

            match_id.delete()

            # error
            if match_res.status_code != 200:
                log["error"] += match_res.text + "\n"
                print("error : ", match_res.text)
                break

            match_data = match_res.json()

            if match_data["info"]["game_type"] != "Ranked":
                print("is not rank match")
                continue

            new_last_matched_at = datetime.strptime(
                match_data["info"]["game_start_time_utc"][:26], "%Y-%m-%dT%H:%M:%S.%f")

            tmp = dict()
            tmp["data_version"] = match_data["metadata"]["data_version"]
            tmp["match_id"] = match_data["metadata"]["match_id"]
            tmp["game_mode"] = match_data["info"]["game_mode"]
            tmp["game_type"] = match_data["info"]["game_type"]
            tmp["game_start_time_utc"] = match_data["info"]["game_start_time_utc"]
            tmp["game_version"] = match_data["info"]["game_version"]

            for player in match_data["info"]["players"]:
                tmp[f"{player['game_outcome']}_user_puuid"] = player["puuid"]
                tmp[f"{player['game_outcome']}_user_deck_id"] = player["deck_id"]
                tmp[f"{player['game_outcome']}_user_deck_code"] = player["deck_code"]
                tmp[f"{player['game_outcome']}_user_order_of_play"] = player["order_of_play"]

            row = []
            for header in header_row:
                row.append(str(tmp.get(header, "")))
            tmp = ", ".join(row) + "\n"
            match_datas.append(tmp)

            for player_puuid in match_data["metadata"]["participants"]:
                db_player: models.Player = db.query(models.Player).filter(
                    models.Player.puuid == player_puuid).first()

                if not db_player:
                    new_player_puuid_sqs.send_message(
                        DelaySeconds=10,
                        MessageBody=(
                            f"{player_puuid}\n{match_id.body}\n{new_last_matched_at}"
                        )
                    )
                    continue

                db_player.last_matched_at = max(
                    db_player.last_matched_at or datetime.min, new_last_matched_at)
                db.commit()
            log["total save data count"] += 1

    return match_datas, log


def save_match_data(match_datas: List[str]) -> None:
    if not match_datas:
        print("no data")
        return

    tmp = ", ".join(header_row) + "\n"

    for match_data in match_datas:
        tmp += match_data

    s3 = boto3.client('s3')
    s3.put_object(
        Bucket="lor-match-data",
        Key=f"{datetime.utcnow().strftime('year=%Y/month=%m/day=%d/hour=%H')}/match_data-1-{uuid.uuid4()}.csv.gz",
        Body=gzip.compress(tmp.encode("utf-8"))
    )


def lambda_handler(event, context):
    match_datas, log = get_match_data_datail()
    log["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    save_match_data(match_datas)

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
                "title": "매치 데이터 저장 로그",
                "description": f"""
                총 `{log["total receive data count"]}`개의 매치 데이터 ID를 받았습니다.
                총 `{log["total save data count"]}`개의 매치 데이터를 저장했습니다.

                error : {f"`{log['error']}`" if log["error"] else ""}
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

import requests
import os
import models
import database
from typing import List, Optional
from sqlalchemy.sql import exists
from sqlalchemy import literal

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")


def lambda_handler(event, context):
    db = database.get_db()

    db_master_players_puuid: List[models.Player] = db.query(
        models.Player).filter(models.Player.is_master == True, models.Player.puuid != None).all()

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
            continue

        match_ids = res.json()

        new_last_match_id: Optional[str] = None
        if match_ids:
            new_last_match_id = match_ids[0]

        for match_id in match_ids:
            if match_id == db_master_player.last_matched_game_id:
                print("Already checked")
                break

            print("match_id", match_id)

            match_res = requests.get(
                f"https://apac.api.riotgames.com/lor/match/v1/matches/{match_id}",
                headers={
                    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Riot-Token": RIOT_API_KEY,
                },
                timeout=3
            )

            if match_res.status_code != 200:
                print(match_res.text)
                if match_res.status_code == 429:
                    print("Too many requests")
                    return
                continue

            match_data = match_res.json()

            print(match_data["info"]["game_type"])

            if match_data["info"]["game_type"] != "Ranked":
                continue

            for puuid in match_data["metadata"]["participants"]:
                if puuid == db_master_player.puuid:
                    continue

                # 이미 DB에 수집된 puuid인지 확인
                if print(db.query(literal(True)).filter(db.query(models.Player).filter(
                    models.Player.puuid == puuid
                ).exists()).scalar()):
                    continue

                account_res = requests.get(
                    f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}",
                    headers={
                        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-Riot-Token": RIOT_API_KEY,
                    },
                    timeout=3
                )
                if account_res.status_code != 200:
                    print(account_res.text)
                    if account_res.status_code == 429:
                        print("Too many requests")
                        return
                    continue
                account_data = account_res.json()

                # 상대가 마스터이고, DB에 수집된 puuid가 없지만 이름이 같은 마스터 유저가 있는지 확인
                db_new_player: models.Player = db.query(models.Player).filter(
                    models.Player.game_name == account_data["gameName"], models.Player.puuid == None).first()

                if db_new_player:
                    print("update", db_new_player.game_name, puuid)

                    db_new_player.puuid = puuid
                    db_new_player.game_name = account_data["gameName"]
                    db_new_player.tag_line = account_data["tagLine"]

                    db.commit()
                    continue

                # 상대가 DB에 아예 없으면 (다이아)
                print("new", account_data["gameName"], puuid)
                db_new_player = models.Player(
                    puuid=puuid,
                    game_name=account_data["gameName"],
                    tag_line=account_data["tagLine"],
                    is_master=False
                )
                db.add(db_new_player)
                db.commit()

        db_master_player.last_matched_game_id = new_last_match_id
        db.commit()
        print("end", db_master_player.puuid)

    db.commit()

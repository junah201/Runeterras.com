import database
import models
import requests
import os
from typing import Tuple, Dict, Optional, List

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")

db = next(database.get_db())

db_players: List[models.Player] = db.query(models.Player).filter(
    models.Player.puuid != None).offset(2900 + 470).all()

total = len(db_players)
for idx, db_player in enumerate(db_players):
    print(f"({idx}/{total}) update {db_player.game_name}#{db_player.tag_line}")
    res = requests.get(
        f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{db_player.game_name}/{db_player.tag_line}",
        headers={
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": RIOT_API_KEY,
        },
        timeout=3
    )
    try:
        if res.status_code == 200:
            db_player.puuid = res.json()["puuid"]
            print(db_player.puuid)
            db.commit()
        elif res.status_code == 404:
            db.delete(db_player)
            db.commit()
        else:
            print(res.status_code)
            print(res.json())
    except Exception as e:
        print(e)
        db.delete(db_player)
        db.commit()

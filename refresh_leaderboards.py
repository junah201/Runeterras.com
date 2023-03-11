import requests
import os
from database import crud, models, database
from typing import List

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")


def lambda_handler(event, context):
    res = requests.get(
        "https://sea.api.riotgames.com/lor/ranked/v1/leaderboards",
        headers={
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": RIOT_API_KEY,
        },
    )

    if res.status_code != 200:
        print(res.text)
        return

    players: List[str] = [player["name"] for player in res.json()["players"]]

    db = database.get_db()

    db_master_players: List[models.Player] = db.query(models.Player).filter(
        models.Player.game_name.in_(players))

    db_master_players.update({models.Player.is_master: True})

    db.query(models.Player).filter(
        models.Player.game_name.not_in(players)
    ).update({models.Player.is_master: False})

    db_master_player_names = set(
        [player.game_name for player in db_master_players])

    for player in players:
        if player not in db_master_player_names:
            print(player)
            db_player = models.Player(
                game_name=player,
                is_master=True,
            )
            db.add(db_player)

    print("end")
    db.commit()


lambda_handler(None, None)

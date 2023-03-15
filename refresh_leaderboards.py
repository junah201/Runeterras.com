import requests
import os
import models
import database
from typing import List, Dict
from datetime import datetime

RIOT_API_KEY = os.environ.get("RIOT_API_KEY")
DISCORD_WEBHOOKS_REFRESH_LEADERBOARDS_LOG = os.environ.get(
    "DISCORD_WEBHOOKS_REFRESH_LEADERBOARDS_LOG")


def refresh_leaderboards() -> Dict:
    log = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "new master players": [],
        "total master players": 0,
        "end": None,
        "rate limit": False,
    }

    res = requests.get(
        "https://sea.api.riotgames.com/lor/ranked/v1/leaderboards",
        headers={
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": RIOT_API_KEY,
        },
    )

    if res.status_code != 200:
        if res.status_code == 429:
            log["rate limit"] = True
        return log

    players: List[str] = [player["name"] for player in res.json()["players"]]
    log["total master players"] = len(players)

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
            log["new master players"].append(f"**{player}**\n")
            db_player = models.Player(
                game_name=player,
                is_master=True,
            )
            db.add(db_player)

    db.commit()
    return log


def lambda_handler(event, context):

    log = refresh_leaderboards()
    log["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "new master players": [],
        "total master players": 0,
        "end": None,
        "rate limit": False,
    }

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
                "title": "Refresh Leaderboards LOG",
                "description": f"""
                총 `{log["total master players"]}`명의 마스터 플레이어가 있습니다.

                새로운 마스터 플레이어 `{len(log["new master players"])}`명을 발견했습니다.
                {"```" + "".join([f"{player}" for player in log["new master players"]]) + "```" if log["new players"] else ""}

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
        DISCORD_WEBHOOKS_REFRESH_LEADERBOARDS_LOG,
        json=data
    )

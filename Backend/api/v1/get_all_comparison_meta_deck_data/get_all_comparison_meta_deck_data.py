import models
import database
import json
from typing import List
from collections import defaultdict
from sqlalchemy.orm import joinedload, aliased


def turns_count(turns: dict) -> dict:
    tmp_turn_data = defaultdict(lambda: {
        "W": 0,
        "L": 0,
    })

    for key, value in turns.items():
        tmp_turn_data[key]["W"] += value["W"]
        tmp_turn_data[key]["L"] += value["L"]

    turn_data = dict()
    for turn_count in range(1, max(len(tmp_turn_data.keys()), 50) + 1):
        turn_data[str(turn_count)] = {
            "W": tmp_turn_data[str(turn_count)]["W"],
            "L": tmp_turn_data[str(turn_count)]["L"],
        }

    return turn_data


def lambda_handler(event, context):
    skip = (event or {}).get("queryStringParameters", {}).get("skip", 0)
    limit = (event or {}).get("queryStringParameters", {}).get("limit", 10)
    game_version = (event or {}).get(
        "queryStringParameters", {}).get("game_version", None)

    db = next(database.get_db())
    if not game_version:
        db_game_version: models.GameVersion = db.query(models.GameVersion).order_by(
            models.GameVersion.game_version.desc()).first()
    else:
        db_game_version: models.GameVersion = db.query(models.GameVersion).filter(
            models.GameVersion.game_version == game_version).first()

    game_version = db_game_version.game_version

    if not db_game_version:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": f"GameVersion (id : {game_version}) Not Found"
                }
            )
        }

    my_deck_alias = aliased(models.SingleMetaDeckAnalyze)
    opponent_deck_alias = aliased(models.SingleMetaDeckAnalyze)

    db_all_meta_deck_analyze: List[models.DoubleMetaDeckAnalyze] = db.query(models.DoubleMetaDeckAnalyze)\
        .join(my_deck_alias, my_deck_alias.id == models.DoubleMetaDeckAnalyze.my_deck_id)\
        .options(joinedload(models.DoubleMetaDeckAnalyze.opponent_deck))\
        .filter(my_deck_alias.game_version == game_version)\
        .join(opponent_deck_alias, opponent_deck_alias.id == models.DoubleMetaDeckAnalyze.opponent_deck_id)\
        .options(joinedload(models.DoubleMetaDeckAnalyze.my_deck))\
        .order_by((models.DoubleMetaDeckAnalyze.win_count + models.DoubleMetaDeckAnalyze.lose_count).desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(
            [
                {
                    "id": data.id,
                    "win_count": data.win_count,
                    "lose_count": data.lose_count,
                    "first_start_win_count": data.first_start_win_count,
                    "first_start_lose_count": data.first_start_lose_count,
                    "turns": turns_count(data.turns),
                    "my_deck": {
                        "id": data.my_deck.id,
                        "game_version": data.my_deck.game_version,
                        "deck_code": data.my_deck.deck_code,
                        "win_count": data.my_deck.win_count,
                        "lose_count": data.my_deck.lose_count,
                        "first_start_win_count": data.my_deck.first_start_win_count,
                        "first_start_lose_count": data.my_deck.first_start_lose_count,
                    },
                    "opponent_deck": {
                        "id": data.opponent_deck.id,
                        "game_version": data.opponent_deck.game_version,
                        "deck_code": data.opponent_deck.deck_code,
                        "win_count": data.opponent_deck.win_count,
                        "lose_count": data.opponent_deck.lose_count,
                        "first_start_win_count": data.opponent_deck.first_start_win_count,
                        "first_start_lose_count": data.opponent_deck.first_start_lose_count,
                    },
                }
                for data in db_all_meta_deck_analyze
            ]
        )
    }

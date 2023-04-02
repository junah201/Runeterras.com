import models
import database
from typing import List
import json
from collections import defaultdict


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
    skip = event.get("queryStringParameters", {}).get("skip", 0)
    limit = event.get("queryStringParameters", {}).get("limit", 10)
    game_version = event.get("queryStringParameters",
                             {}).get("game_version", None)

    db = next(database.get_db())
    if not game_version:
        db_game_version: models.GameVersion = db.query(models.GameVersion).order_by(
            models.GameVersion.game_version.desc()).first()
        game_version = db_game_version.game_version

    db_meta_decks: List[models.SingleMetaDeckAnalyze] = db.query(models.SingleMetaDeckAnalyze).filter(models.SingleMetaDeckAnalyze.game_version == game_version).order_by(
        (models.SingleMetaDeckAnalyze.win_count + models.SingleMetaDeckAnalyze.lose_count).desc()).offset(skip).limit(limit)

    db_meta_decks = db_meta_decks.all()

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(
            [
                {
                    "id": db_meta_deck.id,
                    "game_version": db_meta_deck.game_version,
                    "deck_code": db_meta_deck.deck_code,
                    "win_count": db_meta_deck.win_count,
                    "lose_count": db_meta_deck.lose_count,
                    "first_start_win_count": db_meta_deck.first_start_win_count,
                    "first_start_lose_count": db_meta_deck.first_start_lose_count,
                    "turns": turns_count(db_meta_deck.turns),
                } for db_meta_deck in db_meta_decks
            ]
        )
    }

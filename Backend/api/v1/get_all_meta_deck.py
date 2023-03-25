import models
import database
from typing import List
import json


def lambda_handler(event, context):
    skip = event["queryStringParameters"].get("skip", None)
    limit = event["queryStringParameters"].get("limit", None)

    db = database.get_db()
    db_meta_decks: List[models.SingleMetaDeckAnalyze] = db.query(models.SingleMetaDeckAnalyze).order_by(
        (models.SingleMetaDeckAnalyze.win_count + models.SingleMetaDeckAnalyze.lose_count).asc())

    if skip and limit:
        db_meta_decks = db_meta_decks.offset(skip).limit(limit)

    db_meta_decks = db_meta_decks.all()

    return {
        "statusCode": "200",
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
                } for db_meta_deck in db_meta_decks
            ]
        )
    }

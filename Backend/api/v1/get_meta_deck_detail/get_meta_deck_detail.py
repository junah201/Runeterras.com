import models
import database
from typing import List
import json


def lambda_handler(event, context):
    deck_id = event.get("pathParameters", {}).get("deck_id", None)

    if not deck_id:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": "deck_id is required"
                }
            )
        }

    db = next(database.get_db())
    db_meta_deck: models.SingleMetaDeckAnalyze = db.query(models.SingleMetaDeckAnalyze).filter(
        models.SingleMetaDeckAnalyze.id == deck_id).first()

    if not db_meta_deck:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": f"meta deck (id : {deck_id}) not found"
                }
            )
        }

    db_deck_codes: List[models.SingleMetaDeckCodeAnalyze] = db.query(models.SingleMetaDeckCodeAnalyze)\
        .filter(models.SingleMetaDeckCodeAnalyze.single_meta_deck_analyze_id == deck_id)\
        .order_by(models.SingleMetaDeckCodeAnalyze.win_count.desc())\
        .limit(10)\
        .all()

    deck_code_data: List[dict] = [
        {
            "deck_code": deck_code.deck_code,
            "win": deck_code.win_count,
            "lose": deck_code.lose_count,
        }
        for deck_code in db_deck_codes
    ]

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(
            {
                "id": db_meta_deck.id,
                "deck_code": deck_code_data,
            }
        )
    }

import models
import database
from typing import List
import json


def lambda_handler(event, context):
    db = database.get_db()
    db_champion_cards: List[models.Card] = db.query(models.Card).filter(
        models.Card.is_champion == True).all()

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(
            [
                {
                    "id": db_card.id,
                    "name": db_card.name,
                    "region": db_card.region,
                    "type": db_card.type,
                    "set": db_card.set,
                    "is_champion": db_card.is_champion,
                } for db_card in db_champion_cards
            ]
        )
    }

import models
import database
import json
from lor_deckcodes import LoRDeck, CardCodeAndCount


def lambda_handler(event, context):
    my_deck_cards = event.get("queryStringParameters",
                              {}).get("my_deck_cards", None)
    opponent_deck_cards = event.get("queryStringParameters",
                                    {}).get("opponent_deck_cards", None)
    game_version = event.get("queryStringParameters",
                             {}).get("game_version", None)

    if not my_deck_cards:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": "my_deck_cards is required"
                }
            )
        }

    if not opponent_deck_cards:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": "opponent_deck_cards is required"
                }
            )
        }

    db = next(database.get_db())

    if not game_version:
        db_game_version: models.GameVersion = db.query(models.GameVersion).order_by(
            models.GameVersion.created_at.desc()).first()
    else:
        db_game_version: models.GameVersion = db.query(models.GameVersion).filter(
            models.GameVersion.game_version == game_version).first()

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

    my_deck_cards = sorted(my_deck_cards.split(","))
    opponent_deck_cards = sorted(opponent_deck_cards.split(","))

    my_deck_code = LoRDeck(
        [
            CardCodeAndCount(card_code, 1)
            for card_code in my_deck_cards
        ]
    ).encode()

    opponent_deck_code = LoRDeck(
        [
            CardCodeAndCount(card_code, 1)
            for card_code in opponent_deck_cards
        ]
    ).encode()

    my_deck: models.SingleMetaDeckAnalyze = models.SingleMetaDeckAnalyze(
        deck_code=my_deck_code,
        game_version=game_version
    )

    if not my_deck:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": f"Deck (id : {my_deck_code}) Not Found"
                }
            )
        }

    opponent_deck: models.SingleMetaDeckAnalyze = models.SingleMetaDeckAnalyze(
        deck_code=opponent_deck_code,
        game_version=game_version
    )

    if not opponent_deck:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": f"Deck (id : {opponent_deck_code}) Not Found"
                }
            )
        }

    db_double_meta_deck_analyze: models.DoubleMetaDeckCodeAnalyze = db.query(
        models.DoubleMetaDeckCodeAnalyze).filter(
            models.DoubleMetaDeckCodeAnalyze.my_deck_id == my_deck.id,
            models.DoubleMetaDeckCodeAnalyze.opponent_deck_id == opponent_deck.id,
    ).first()

    if not db_double_meta_deck_analyze:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": f"DoubleMetaDeckCodeAnalyze (id : {my_deck_code} vs {opponent_deck_code}) Not Found"
                }
            )
        }

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(
            {
                "id": db_double_meta_deck_analyze.id,
                "my_deck_id": db_double_meta_deck_analyze.my_deck_id,
                "opponent_deck_id": db_double_meta_deck_analyze.opponent_deck_id,
                "win_count": db_double_meta_deck_analyze.win_count,
                "lose_count": db_double_meta_deck_analyze.lose_count
            }
        )
    }

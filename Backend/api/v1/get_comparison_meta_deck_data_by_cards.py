import models
import database
import json
from lor_deckcodes import LoRDeck, CardCodeAndCount
from typing import List
from collections import defaultdict


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

    my_deck: models.SingleMetaDeckAnalyze = db.query(models.SingleMetaDeckAnalyze).filter(
        models.SingleMetaDeckAnalyze.deck_code == my_deck_code,
        models.SingleMetaDeckAnalyze.game_version == db_game_version.game_version
    ).first()

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

    opponent_deck: models.SingleMetaDeckAnalyze = db.query(models.SingleMetaDeckAnalyze).filter(
        models.SingleMetaDeckAnalyze.deck_code == opponent_deck_code,
        models.SingleMetaDeckAnalyze.game_version == db_game_version.game_version
    ).first()

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

    db_double_meta_deck_analyze: models.DoubleMetaDeckAnalyze = db.query(
        models.DoubleMetaDeckAnalyze).filter(
            models.DoubleMetaDeckAnalyze.my_deck_id == my_deck.id,
            models.DoubleMetaDeckAnalyze.opponent_deck_id == opponent_deck.id,
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
                    "message": f"DoubleMetaDeckCodeAnalyze (id : {my_deck_code} ({my_deck.id}) vs {opponent_deck_code} ({opponent_deck.id})) Not Found"
                }
            )
        }

    db_turns: List[models.DoubleMetaDeckTurnAnalyze] = db.query(models.DoubleMetaDeckTurnAnalyze)\
        .filter(models.DoubleMetaDeckTurnAnalyze.double_meta_deck_analyze_id == db_double_meta_deck_analyze.id)\
        .order_by(models.DoubleMetaDeckTurnAnalyze.turn_count)\
        .all()

    tmp_turn_data = defaultdict(lambda: {
        "win": 0,
        "lose": 0,
    })

    for turn in db_turns:
        tmp_turn_data[turn.turn_count]["win"] += turn.win_count
        tmp_turn_data[turn.turn_count]["lose"] += turn.lose_count

    turn_data = dict()
    for turn_count in range(1, max(tmp_turn_data.keys()) + 1):
        turn_data[turn_count] = {
            "win": tmp_turn_data[turn_count]["win"],
            "lose": tmp_turn_data[turn_count]["lose"],
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
                "lose_count": db_double_meta_deck_analyze.lose_count,
                "first_start_win_count": db_double_meta_deck_analyze.first_start_win_count,
                "first_start_lose_count": db_double_meta_deck_analyze.first_start_lose_count,
                "turn": turn_data,
            }
        )
    }

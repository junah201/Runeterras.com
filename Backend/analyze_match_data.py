import os
import models
import database
from datetime import datetime, timedelta
from typing import Dict, Union, List, Optional
import boto3
from collections import defaultdict
from csv import DictReader
from lor_deckcodes import LoRDeck, CardCodeAndCount
import requests
import gzip
import io
from urllib.parse import unquote_plus

DISCORD_WEBHOOKS_ANALYZE_MATCH_DATA_LOG = os.environ.get(
    "DISCORD_WEBHOOKS_ANALYZE_MATCH_DATA_LOG")


def analyze_match_data(s3_bucket: str, s3_path: str) -> int:
    total_match_count = 0

    s3_client = boto3.client('s3')

    obj = s3_client.get_object(
        Bucket=s3_bucket, Key=s3_path)

    with gzip.GzipFile(fileobj=io.BytesIO(obj["Body"].read()), mode='rb') as fh:
        lines = fh.read().decode("utf-8").split()

    total_match_count = len(lines) - 1

    game_version_analyze = defaultdict(lambda: {
        "total_match_count": 0,
    })

    single_meta_deck_analyze = defaultdict(
        lambda:
        {
            "win": 0,
            "lose": 0,
            "turn": defaultdict(
                lambda:
                {
                    "win": 0,
                    "lose": 0,
                }
            ),
            "single_meta_deck_code_analyze": defaultdict(
                lambda:
                {
                    "win": 0,
                    "lose": 0,
                }
            ),
            "first_start_win_count": 0,
            "first_start_lose_count": 0,
        }
    )

    double_meta_deck_analyze = defaultdict(
        lambda:
        {
            "win": 0,
            "lose": 0,
        }
    )

    db = database.get_db()
    db_card_champions: List[models.Card] = db.query(models.Card).filter(
        models.Card.is_champion == True).all()

    all_card_champion_ids = set([card.id for card in db_card_champions])

    for row in DictReader(lines):
        print(f"finding : {row['match_id']}")
        game_version_analyze[row["game_version"]]["total_match_count"] += 1

        winner_deck = LoRDeck.from_deckcode(
            row["win_user_deck_code"])
        winner_new_deck_code = LoRDeck(
            [
                CardCodeAndCount(card.card_code, 1) for card in winner_deck.cards if card.card_code in all_card_champion_ids
            ]
        ).encode()

        loser_deck = LoRDeck.from_deckcode(
            row["loss_user_deck_code"])
        loser_new_deck_code = LoRDeck(
            [
                CardCodeAndCount(card.card_code, 1) for card in loser_deck.cards if card.card_code in all_card_champion_ids
            ]
        ).encode()

        single_meta_deck_analyze[(row["game_version"], winner_new_deck_code)
                                 ]["win"] += 1
        single_meta_deck_analyze[(row["game_version"], winner_new_deck_code)
                                 ]["turn"][row["total_turn_count"]]["win"] += 1
        single_meta_deck_analyze[(row["game_version"], winner_new_deck_code)
                                 ]["single_meta_deck_code_analyze"][row["win_user_deck_code"]]["win"] += 1

        is_first_start = (int(row["total_turn_count"]) %
                          2 == int(row["win_user_order_of_play"]))
        if is_first_start:
            single_meta_deck_analyze[(row["game_version"], winner_new_deck_code)
                                     ]["first_start_win_count"] += 1

        single_meta_deck_analyze[(row["game_version"], loser_new_deck_code)
                                 ]["lose"] += 1
        single_meta_deck_analyze[(row["game_version"], loser_new_deck_code)
                                 ]["turn"][row["total_turn_count"]]["lose"] += 1
        single_meta_deck_analyze[(row["game_version"], winner_new_deck_code)
                                 ]["single_meta_deck_code_analyze"][row["loss_user_deck_code"]]["lose"] += 1

        is_first_start = (int(row["total_turn_count"]) %
                          2 == int(row["loss_user_order_of_play"]))
        if is_first_start:
            single_meta_deck_analyze[(row["game_version"], loser_new_deck_code)
                                     ]["first_start_lose_count"] += 1

        double_meta_deck_analyze[(
            row["game_version"], winner_new_deck_code, loser_new_deck_code)]["win"] += 1
        double_meta_deck_analyze[(
            row["game_version"], loser_new_deck_code, winner_new_deck_code)]["lose"] += 1

    for key, value in game_version_analyze.items():
        db_game_version = db.query(models.GameVersion).filter(
            models.GameVersion.game_version == key).first()

        if not db_game_version:
            db_game_version = models.GameVersion(
                game_version=key,
            )
            db.add(db_game_version)
            db.commit()
            db.refresh(db_game_version)

        db_game_version.total_match_count += value["total_match_count"]
        db.commit()

    for key, value in single_meta_deck_analyze.items():
        db_single_meta_deck_analyze = db.query(models.SingleMetaDeckAnalyze).filter(
            models.SingleMetaDeckAnalyze.game_version == key[0],
            models.SingleMetaDeckAnalyze.deck_code == key[1],
        ).first()

        if not db_single_meta_deck_analyze:
            db_single_meta_deck_analyze = models.SingleMetaDeckAnalyze(
                game_version=key[0],
                deck_code=key[1],
            )
            db.add(db_single_meta_deck_analyze)
            db.commit()
            db.refresh(db_single_meta_deck_analyze)

        db_single_meta_deck_analyze.win_count += value["win"]
        db_single_meta_deck_analyze.lose_count += value["lose"]
        db_single_meta_deck_analyze.first_start_win_count = value["first_start_win_count"]
        db_single_meta_deck_analyze.first_start_lose_count = value["first_start_lose_count"]

        for turn_key, turn_value in value["turn"].items():
            db_single_meta_deck_turn_analyze = db.query(models.SingleMetaDeckTurn).filter(
                models.SingleMetaDeckTurn.single_meta_deck_analyze_id == db_single_meta_deck_analyze.id,
                models.SingleMetaDeckTurn.turn_count == turn_key,
            ).first()

            if not db_single_meta_deck_turn_analyze:
                db_single_meta_deck_turn_analyze = models.SingleMetaDeckTurn(
                    single_meta_deck_analyze_id=db_single_meta_deck_analyze.id,
                    turn_count=turn_key,
                )
                db.add(db_single_meta_deck_turn_analyze)
                db.commit()
                db.refresh(db_single_meta_deck_turn_analyze)

            db_single_meta_deck_turn_analyze.win_count += turn_value["win"]
            db_single_meta_deck_turn_analyze.lose_count += turn_value["lose"]
            db.commit()

        for single_meta_deck_code_analyze_key, single_meta_deck_code_analyze_value in value["single_meta_deck_code_analyze"].items():
            db_single_meta_deck_code_analyze = db.query(models.SingleMetaDeckCodeAnalyze).filter(
                models.SingleMetaDeckCodeAnalyze.game_version == key[0],
                models.SingleMetaDeckCodeAnalyze.single_meta_deck_analyze_id == db_single_meta_deck_analyze.id,
                models.SingleMetaDeckCodeAnalyze.deck_code == single_meta_deck_code_analyze_key,
            ).first()

            if not db_single_meta_deck_code_analyze:
                db_single_meta_deck_code_analyze = models.SingleMetaDeckCodeAnalyze(
                    game_version=key[0],
                    single_meta_deck_analyze_id=db_single_meta_deck_analyze.id,
                    deck_code=single_meta_deck_code_analyze_key,
                )
                db.add(db_single_meta_deck_code_analyze)
                db.commit()
                db.refresh(db_single_meta_deck_code_analyze)

            db_single_meta_deck_code_analyze.win_count += single_meta_deck_code_analyze_value["win"]
            db_single_meta_deck_code_analyze.lose_count += single_meta_deck_code_analyze_value["lose"]
            db.commit()

        db.commit()

    for key, value in double_meta_deck_analyze.items():
        db_winner_single_meta_deck_analyze: models.SingleMetaDeckAnalyze = db.query(models.SingleMetaDeckAnalyze).filter(
            models.SingleMetaDeckAnalyze.game_version == key[0],
            models.SingleMetaDeckAnalyze.deck_code == key[1],
        ).first()

        db_loser_single_meta_deck_analyze: models.SingleMetaDeckAnalyze = db.query(models.SingleMetaDeckAnalyze).filter(
            models.SingleMetaDeckAnalyze.game_version == key[0],
            models.SingleMetaDeckAnalyze.deck_code == key[2],
        ).first()

        db_double_meta_deck_analyze: Optional[models.DoubleMetaDeckCodeAnalyze] = db.query(models.DoubleMetaDeckCodeAnalyze).filter(
            models.DoubleMetaDeckCodeAnalyze.my_deck_id == db_winner_single_meta_deck_analyze.id,
            models.DoubleMetaDeckCodeAnalyze.opponent_deck_id == db_loser_single_meta_deck_analyze.id,
        ).first()

        if not db_double_meta_deck_analyze:
            db_double_meta_deck_analyze = models.DoubleMetaDeckCodeAnalyze(
                my_deck_id=db_winner_single_meta_deck_analyze.id,
                opponent_deck_id=db_loser_single_meta_deck_analyze.id,
            )
            db.add(db_double_meta_deck_analyze)
            db.commit()
            db.refresh(db_double_meta_deck_analyze)

        db_double_meta_deck_analyze.win_count += value["win"]
        db_double_meta_deck_analyze.lose_count += value["lose"]

    db.commit()

    return total_match_count


def lambda_handler(event, context):
    log = {
        "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_match_count": 0,
        "target_files": [],
        "end": None,
    }

    total_match_count = 0

    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = unquote_plus(record['s3']['object']['key'])
        log["target_files"].append(s3_key)
        print(f"Match data path: {s3_bucket} {s3_key}")
        total_match_count += analyze_match_data(s3_bucket, s3_key)

    log["total_match_count"] = total_match_count
    log["end"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    success_color = 0x2ECC71

    requests.post(
        DISCORD_WEBHOOKS_ANALYZE_MATCH_DATA_LOG,
        json={
            "content": "",
            "embeds": [
                {
                    "title": "매치 데이터 분석 로그",
                    "description": f"""
                총 `{log["total_match_count"]}`개의 매치를 분석하였습니다..

                target file : `{log["target_files"]}`

                시작 : `{log["start"]}`
                종료 : `{log["end"]}`
                """,
                    "color": success_color,
                    "footer": {
                        "text": str(log["start"])
                    }
                }
            ]
        }
    )

    return log

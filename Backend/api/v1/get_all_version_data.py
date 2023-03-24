import requests
import os
import models
import database
from datetime import datetime
from typing import Dict, List
import boto3
from sqlalchemy import literal
from sqlalchemy.sql import exists


def lambda_handler(event, context):
    db = database.get_db()
    db_game_versions: List[models.GameVersion] = db.query(models.GameVersion).order_by(
        models.GameVersion.created_at.desc()).all()

    return {
        "statusCode": 200,
        "body": [
            {
                "game_version": db_game_version.game_version,
                "total_match_count": db_game_version.total_match_count,
                "created_at": db_game_version.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": db_game_version.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            } for db_game_version in db_game_versions
        ]
    }

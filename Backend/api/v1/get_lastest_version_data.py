import models
import database
import json


def lambda_handler(event, context):
    db = database.get_db()
    db_game_version: models.GameVersion = db.query(models.GameVersion).order_by(
        models.GameVersion.created_at.desc()).first()

    return {
        "statusCode": "200",
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(
            {
                "game_version": db_game_version.game_version,
                "total_match_count": db_game_version.total_match_count,
                "created_at": db_game_version.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": db_game_version.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    }

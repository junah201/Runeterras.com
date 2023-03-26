import models
import database
import json


def lambda_handler(event, context):
    gmae_version = event.get("pathParameters", {}).get("game_version", None)

    if not gmae_version:
        return {
            "statusCode": "400",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": "gmae_version is required"
                }
            )
        }

    db = database.get_db()
    db_game_version: models.GameVersion = db.query(models.GameVersion).filter(
        models.GameVersion.game_version == gmae_version).first()

    if not db_game_version:
        return {
            "statusCode": "404",
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(
                {
                    "message": f"GameVersion (id : {gmae_version}) Not Found"
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
                "game_version": db_game_version.game_version,
                "total_match_count": db_game_version.total_match_count,
                "created_at": db_game_version.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": db_game_version.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    }

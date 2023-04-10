import json
import requests
import models
import database

with open("en_us.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

db = next(database.get_db())

for idx, value in enumerate(data.values()):
    db_card = db.query(models.Card).filter(
        models.Card.id == value.get("cardCode")).first()

    if db_card:
        continue

    print(idx, len(data))
    print(value.get("cardCode"))

    db_card = models.Card(
        id=value.get("cardCode"),
        name=value.get("name"),
        region=value.get("regions")[0],
        type=value.get("type"),
        set=value.get("set"),
        is_champion=False,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)

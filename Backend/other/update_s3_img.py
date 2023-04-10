import json
import requests
import boto3
import os

with open("ko_kr.json", "r", encoding="utf-8-sig") as f:
    data = json.load(f)

s3 = boto3.resource(
    's3',
    aws_access_key_id=os.environ.get("aws_access_key_id"),
    aws_secret_access_key=os.environ.get("aws_secret_access_key")
)
bucket = s3.Bucket('cdn.runeterras.com')

for idx, value in enumerate(data.values()):
    print(idx, len(data))
    print(value.get("cardCode"))
    response = requests.get(value.get("artPath")[0])
    image_data = response.content

    bucket.put_object(
        Key=f'images/card/ko/{value.get("cardCode")}.png',
        Body=image_data,
        ContentType='image/png'
    )

    response = requests.get(value.get("fullArtPath")[0])
    image_data = response.content

    bucket.put_object(
        Key=f'images/card/ko/{value.get("cardCode")}-full.png',
        Body=image_data,
        ContentType='image/png'
    )

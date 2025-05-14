import boto3
from fastapi import UploadFile

import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")


def upload_to_s3(file: UploadFile, filename: str) -> str:
    # AWS S3에 접근할 수 있도록 boto3 클라이언트를 생성한다.
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    # 파일 객체를 S3에 업로드한다.
    # public-read로 설정하면 누구나 URL로 접근이 가능하다.
    s3.upload_fileobj(file.file, S3_BUCKET, filename, ExtraArgs={"ACL": "public-read"})

    return f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"

def delete_from_s3(filename: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    s3.delete_object(Bucket=S3_BUCKET, Key=filename)
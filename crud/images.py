import uuid
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.s3 import upload_to_s3


# def create_images(
#         db: Session,
#         product_id: int,
#         image_files: List[UploadFile]):
#     for image_file in image_files:
#         ext = image_file.filename.split('.')[-1]
#         filename = f"{uuid.uuid4()}.{ext}"
#         img_url = upload_to_s3(image_file, filename)
#         from models import Image
#         image = Image(
#             product_id=product_id,
#             img_url=img_url
#         )
#         try:
#             db.add(image)
#         except Exception as e:
#             db.rollback()
#             print(f"[Image 저장 실패] {e}")
#             continue
#     db.commit()

def create_images(
        db: Session,
        product_id: int,
        img_url: str
):
    from models import Image
    images = Image(
        product_id = product_id,
        img_url = img_url
    )
    db.add(images)
    db.commit()
    db.refresh(images)
    return images
import uuid

from models.image import Image
from core.s3 import upload_to_s3, delete_from_s3
from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import List


def create_image(db: Session, item_id: int, image_files: List[UploadFile]):
    for image_file in image_files:
        ext = image_file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        img_url = upload_to_s3(image_file, filename)
        image = Image(
            item_id=item_id,
            img_url=img_url
        )
        try:
            db.add(image)
        except Exception as e:
            db.rollback()
            print(f"[Image 저장 실패] {e}")
            continue
    db.commit()



def delete_image_by_id(db: Session, image_id: int):
    image = db.query(Image).filter(Image.image_id == image_id).first()
    if not image:
        return
    try:
        filename = image.img_url.split("/")[-1]
        delete_from_s3(filename)
        db.delete(image)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"[Image 삭제 실패] {e}")
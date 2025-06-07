
from sqlalchemy.orm import joinedload
from models.item import Item
from schemas.item import CreateItem
from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import List
from models.image import Image
from crud.image import delete_image_by_id
from crud.images import create_images

#
# def create_item(db: Session, item: CreateItem, image_files: List[UploadFile]):
#     item = Item(
#         category_name=item.category_name,
#         product_name=item.product_name,
#         product_info=item.product_info,
#         collection_id=item.collection_id
#     )
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     create_image(db, item.item_id, image_files)
#     return item


def find_item_by_id(db: Session, item_id: int):
    item = db.query(Item)\
        .options(joinedload(Item.images))\
        .filter(Item.item_id == item_id)\
        .first()
    return item

def delete_item_by_id(db: Session, item_id: int):
    item = db.query(Item).filter(Item.item_id == item_id).first()
    db.delete(item)
    db.commit()
    return item
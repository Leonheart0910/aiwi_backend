from sqlalchemy.orm import Session
from models.collection import Collection
from models.item import Item
from models.product import Product
from schemas.collection import CollectionCreate
from sqlalchemy.orm import joinedload
from crud.item import delete_item_by_id
from fastapi import HTTPException


def create_collection(db: Session, collection: CollectionCreate):
    collection = Collection(
        collection_title=collection.collection_title,
        user_id=collection.user_id,
    )
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

def get_collection_with_items(db: Session, collection_id: int):
    return db.query(Collection)\
        .options(
            joinedload(Collection.items).
            joinedload(Item.product).
            joinedload(Product.product_info).
            joinedload(Product.image)
        )\
        .filter(Collection.collection_id == collection_id)\
        .first()

def delete_collection_by_id(db: Session, collection_id: int):
    collection = db.query(Collection).filter(Collection.collection_id == collection_id).first()
    if collection:
        for item in collection.items:
            delete_item_by_id(db, item.item_id)
        db.delete(collection)
        db.commit()
    return collection

def delete_collection_items_by_id(db: Session,
                                  collection_id: int,
                                  item_id: int):
    collection = db.query(Collection).filter(Collection.collection_id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="장바구니를 찾을 수 없습니다")

    item = db.query(Item).filter(
        Item.item_id == item_id,
        Item.collection_id == collection_id  # ← 이게 핵심
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="아이템이 장바구니 안에 없습니다")

    try:
        product_name = item.product.product_name
    except AttributeError:
        # 만약 item.product_name 속성을 직접 가지고 있다면 바로 꺼내도 됨
        product_name = getattr(item, "product_name", "")


    db.delete(item)
    db.commit()

    return {"message": f"{collection.collection_title}에 들어있는 {product_name} 가 삭제되었습니다."}
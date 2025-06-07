from sqlalchemy import BIGINT
from sqlalchemy.orm import Session
from fastapi import HTTPException

from constant.message.error_message import ErrorMessage
from crud.item import create_item
from exception.exception import OperatedException, ErrorCode
from models.item import Item
from models.product import Product
from schemas.cart_response import CartResponse, ItemOut, CollectionOut
from schemas.collection import CollectionCreate, CollectionResponse, CollectionItemList
from crud.collection import create_collection, delete_collection_by_id, get_collection_with_items, \
    delete_collection_items_by_id
from schemas.collection_summary import CollectionSummaryOut
from models import ProductInfo
from schemas.item import ItemInfo
from models.collection import Collection
from schemas.collection_item_list import *
import logging
from sqlalchemy.orm import load_only

def collection_create_service(
        user_id: int,
        collection_title: str,
        db: Session
):
    try:
        collection_data = CollectionCreate(
            collection_title = collection_title,
            user_id = user_id,
        )

        created_collection = create_collection(db, collection_data)
        if not created_collection:
            raise OperatedException(
                status_code=500,
                error_code=ErrorCode.COLLECTION_CREATE_FAIL.value,
                detail=ErrorMessage.COLLECTION_CREATE_FAIL.value
            )
        return CollectionResponse(
            collection_id= created_collection.collection_id,
            collection_title= created_collection.collection_title,
            user_id= created_collection.user_id,
            created_at= created_collection.created_at,
            updated_at= created_collection.updated_at,
        )
    except OperatedException:
        raise OperatedException(
            status_code=500,
            error_code=ErrorCode.COLLECTION_CREATE_FAIL.value,
            detail=ErrorMessage.COLLECTION_CREATE_FAIL.value
        )

def collection_delete_service(
    collection_id: int,
    db: Session
):
    try:
        collection = delete_collection_by_id(db, collection_id)
        if not collection:
            raise OperatedException(
                status_code=404,
                error_code=ErrorCode.COLLECTION_NOT_FOUND.value,
                detail=ErrorMessage.COLLECTION_NOT_FOUND.value
            )
        else:
            return {"message": f"{collection.collection_title}이 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_collection_items_service(collection_id: int, db: Session) -> CollectionItemList:
    coll: Collection = get_collection_with_items(db, collection_id)

    if coll is None:
        raise OperatedException(
            status_code=404,
            error_code=ErrorCode.COLLECTION_NOT_FOUND.value,
            detail=ErrorMessage.COLLECTION_NOT_FOUND.value
        )

    items_dto: list[ItemInfo] = []
    for item in coll.items:
        info = item.product.product_info
        img_obj = item.product.image
        image_dto = (
            ImageInfo(
                image_id=img_obj.image_id,
                image_url=img_obj.img_url,
                created_at=img_obj.created_at
            )
            if img_obj else None
        )

        items_dto.append(
            ItemInfo(
                item_id=item.item_id,
                product_name=info.product_name,
                product_info=info.product_name,
                product_link=info.product_link,
                category_name=info.product_name,
                created_at=item.created_at,
                image=image_dto
            )
        )

    return CollectionItemList(
        collection_id=coll.collection_id,
        collection_title=coll.collection_title,
        user_id=coll.user_id,
        created_at=coll.created_at,
        items=items_dto
    )


def delete_collection_item_service(
    collection_id: int,
    item_id: int,
    db: Session
):
    try:
        return delete_collection_items_by_id(db= db, collection_id=collection_id, item_id=item_id)
    except OperatedException :
        raise OperatedException(
            status_code=500,
            error_code=ErrorCode.ITEM_IN_COLLECTION_DELETE_FAIL.value,
            detail=ErrorMessage.ITEM_IN_COLLECTION_DELETE_FAIL.value
        )

def add_item_service(
    user_id: int,
    collection_id: id,
    product_id: int,
    db: Session
) -> CartResponse:

    collection = (
        db.query(Collection)
        .filter(Collection.user_id == user_id,
                Collection.collection_id == collection_id)
        .first()
    )
    if collection is None:
        collection = create_collection(db=db,
                                       collection = CollectionCreate(collection_title="임의 장바구니",user_id=user_id))
    # 2. 아이템 저장
    item = Item(
        collection_id=collection.collection_id,
        product_id=product_id)
    db.add(item)
    db.commit()
    db.refresh(item)

    # 3. 방금 저장한 아이템 + 상품 정보 로딩
    from sqlalchemy.orm import selectinload
    item_row = (
        db.query(Item)
        .options(
            selectinload(Item.product)
            .selectinload(Product.product_info)   # ← ⭐ 클래스 말고 속성
        )
        .filter(Item.item_id == item.item_id)
        .one()
    )

    info = item_row.product.product_info

    item_dto = ItemOut(
        item_id=item_row.item_id,
        item_name=info.product_name if info else "",
        created_at=item_row.created_at,
        updated_at=item_row.updated_at,
    )

    col_dto = CollectionOut(
        collection_id=collection.collection_id,
        collection_title=collection.collection_title,
        created_at=collection.created_at,
        updated_at=collection.updated_at,
    )

    return CartResponse(
        user_id=user_id,
        collection=[col_dto],
        item=[item_dto],
    )


def get_collection_list_service(
    user_id: int,
    db: Session
) -> list[CollectionSummaryOut]:
    from sqlalchemy import case
    collections = (
        db.query(Collection)
        .options(load_only(Collection.collection_id,
                           Collection.collection_title,
                           Collection.updated_at))
        .filter(Collection.user_id == user_id)
        .order_by(
            case((Collection.updated_at == None, 1), else_=0),
            Collection.updated_at.desc()
        )
        .all()
    )
    return [
        CollectionSummaryOut(
            collection_id=c.collection_id,
            title=c.collection_title,
            updated_at=c.updated_at
        )
        for c in collections
    ]


def register_item_in_collection_service(
        user_id: int,
        collection_id: int,
        product_id: int,
        db: Session
):
    item = create_item(
        collection_id=collection_id,
        product_id=product_id,
        db=db
    )
    collection = db.query(Collection).filter(Collection.collection_id == collection_id).first()
    product_info = db.query(ProductInfo).filter(ProductInfo.product_id == product_id).first()

    if not collection:
        raise ValueError(f"Collection {collection_id} not found")
    if not product_info:
        raise ValueError(f"ProductInfo {product_id} not found")

    return {
        "user_id": user_id,
        "collection": [{
            "collection_id": collection.collection_id,
            "collection_title": collection.collection_title,
            "created_at": str(collection.created_at),
            "updated_at": str(collection.updated_at),
        }],
        "item": [{
            "item_id": item.item_id,
            "item_name": product_info.product_name,
            "created_at": str(item.created_at),
            "updated_at": str(item.updated_at),
        }]
    }

from sqlalchemy.orm import Session
from fastapi import HTTPException

from api.message.error_message import ErrorMessage
from exception.exception import OperatedException, ErrorCode
from schemas.collection import CollectionCreate, CollectionResponse, CollectionItemList
from crud.collection import create_collection, delete_collection_by_id, get_collection_with_items, \
    delete_collection_items_by_id
from schemas.image import ImageInfo
from schemas.item import ItemInfo


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

def get_collection_items_service(
        collection_id: int,
        db: Session
):
    try:
        info_list = get_collection_with_items(collection_id=collection_id, db=db)

        if not info_list:
            raise OperatedException(
                status_code=404,
                error_code=ErrorCode.COLLECTION_ITEMS_INFORMATION_FAIL.value,
                detail=ErrorMessage.COLLECTION_ITEMS_INFORMATION_FAIL.value
            )

        return CollectionItemList(
            collection_id=info_list.collection_id,
            collection_title=info_list.collection_title,
            user_id=info_list.user_id,
            created_at=info_list.created_at,
            items=[
                ItemInfo(
                    item_id=item.item_id,
                    category_name=item.category_name,
                    product_name=item.product_name,
                    product_info=item.product_info,
                    created_at=item.created_at,
                    image=[
                        ImageInfo(
                            item_id=image.item_id,
                            img_url=image.img_url,
                            created_at=image.created_at
                        ) for image in item.images
                    ]
                ) for item in info_list.items
            ]
        )

    except OperatedException:
        raise OperatedException(
            status_code=500,
            error_code=ErrorCode.ITEM_IN_COLLECTION_INFORMATION_FAIL.value,
            detail=ErrorMessage.ITEM_IN_COLLECTION_INFORMATION_FAIL.value
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
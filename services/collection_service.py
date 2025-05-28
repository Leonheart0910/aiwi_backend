
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.collection import CollectionCreate, CollectionResponse, CollectionItemList
from crud.collection import create_collection, delete_collection_by_id, get_collection_with_items
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
            raise HTTPException(status_code=400, detail="장바구니가 만들어지지 않았습니다.")

        return CollectionResponse(
            collection_id= created_collection.collection_id,
            collection_title= created_collection.collection_title,
            user_id= created_collection.user_id,
            created_at= created_collection.created_at,
            updated_at= created_collection.updated_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def collection_delete_service(
    collection_id: int,
    db: Session
):
    try:
        collection = delete_collection_by_id(db, collection_id)
        if not collection:
            raise HTTPException(status_code=404, detail="존재하지 않는 장바구니입니다.")
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
            raise HTTPException(status_code=404, detail="Collection not found")

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

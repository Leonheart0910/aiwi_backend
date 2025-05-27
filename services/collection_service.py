
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.collection import CollectionCreate, CollectionResponse
from crud.collection import create_collection

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
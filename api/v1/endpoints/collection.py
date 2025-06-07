
from fastapi import APIRouter, Query, Form, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.collection import CollectionCreateRequest
from schemas.item import ItemSaveRequest
from services.collection_service import collection_create_service, get_collection_items_service, \
    delete_collection_item_service, collection_delete_service, get_collection_list_service, \
    register_item_in_collection_service

router = APIRouter()


@router.post(
    "/collection/create"
)
def create_collection(
        request : CollectionCreateRequest,
        db : Session = Depends(get_db)
):
    return collection_create_service(
        user_id=request.user_id,
        collection_title=request.collection_title,
        db = db)



@router.delete(
    "/collection/{collection_id}"
)
def delete_collection(
        collection_id: int,
        db : Session = Depends(get_db)
):
    return collection_delete_service(collection_id, db)

@router.get(
    "/collection/{collection_id}"
)
def get_collection_items(
        collection_id: int,
        db : Session = Depends(get_db)
):
    return get_collection_items_service(
        collection_id=collection_id,
        db=db
    )

@router.delete(
    "/collection/{collection_id}/{item_id}"
)
def delete_collection_item(
        collection_id: int,
        item_id: int,
        db : Session = Depends(get_db)
):
    return delete_collection_item_service(collection_id=collection_id, item_id=item_id, db=db)

@router.get("/collection/list/{user_id}")
def get_collection_list(
        user_id: int,
        db: Session = Depends(get_db)
):

    return get_collection_list_service(
        user_id=user_id,
        db=db)

@router.post("/collection/register")
def register_item_in_collection(
        request : ItemSaveRequest,
        db : Session = Depends(get_db)
):
    return register_item_in_collection_service(
        user_id=request.user_id,
        collection_id=request.collection_id,
        product_id= request.product_id,
        db=db
    )
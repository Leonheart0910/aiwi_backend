
from fastapi import APIRouter, Query, Form, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.collection import CollectionCreateRequest
from services.collection_service import collection_create_service, get_collection_items_service, \
    delete_collection_item_service

router = APIRouter()


@router.post(
    "/collection/create"
)
def create_collection(
        request : CollectionCreateRequest,
        db : Session = Depends(get_db)
):
    try:
        return collection_create_service(db, request.data)
    except HTTPException as e:
        raise e


@router.delete(
    "/collection/{collection_id}"
)
def delete_collection(
        collection_id: int,
        db : Session = Depends(get_db)
):
    return delete_collection(collection_id, db)

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
    try:
        return delete_collection_item_service(collection_id=collection_id, item_id=item_id, db=db)
    except HTTPException as e:
        raise e

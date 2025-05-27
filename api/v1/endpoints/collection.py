
from fastapi import APIRouter, Query, Form, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.collection import CollectionCreateRequest
from services.collection_service import collection_create_service
router = APIRouter()


@router.post(
    "/collection/create"
)
def create_collection(
        request : CollectionCreateRequest,
        db : Session = Depends(get_db)
):
    try:
        collection = collection_create_service(db, request.data)
        return collection
    except HTTPException as e:
        raise e



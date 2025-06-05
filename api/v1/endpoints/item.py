from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.item import ItemSaveRequest
from services.collection_service import add_item_service

router = APIRouter()


@router.post("/item/register")
def item_save(
    request: ItemSaveRequest,
    db: Session = Depends(get_db)
):
    response = add_item_service(
        user_id=request.user_id,
        collection_id = request.collections_id,
        product_id = request.product_id,
        db=db
    )
    return response

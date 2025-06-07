from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from schemas.item import ItemSaveRequest
from services.collection_service import add_item_service

router = APIRouter()




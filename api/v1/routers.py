from fastapi import APIRouter
from .endpoints import naver, user, collection

router = APIRouter()

router.include_router(naver.router, tags=["Naver Shopping"])
router.include_router(user.router, tags=["User"])
router.include_router(collection.router, tags=["Collection"])

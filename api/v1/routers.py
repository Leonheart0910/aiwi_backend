from fastapi import APIRouter
from .endpoints import naver, user, collection, chat

router = APIRouter()

router.include_router(naver.router, tags=["Naver Shopping"])
router.include_router(user.router, tags=["User"])
router.include_router(collection.router, tags=["Collection"])

router.include_router(chat.router, tags=["Chat"])
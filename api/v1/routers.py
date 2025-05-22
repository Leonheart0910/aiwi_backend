from fastapi import APIRouter
from .endpoints import naver, user

router = APIRouter()

router.include_router(naver.router, tags=["Naver Shopping"])
router.include_router(user.router, tags=["User"])

from fastapi import APIRouter
from .endpoints import naver

router = APIRouter()

router.include_router(naver.router, tags=["Naver Shopping"])

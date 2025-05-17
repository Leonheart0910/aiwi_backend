from fastapi import APIRouter, Query, HTTPException
from services.naver_api import search_naver_shopping

router = APIRouter()

@router.get("/naver/search")
def naver_search(query: str = Query(..., description="검색어")):
    result = search_naver_shopping(query)
    if not result:
        raise HTTPException(status_code=500, detail="네이버 API 호출 실패")
    return result

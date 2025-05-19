from typing import Optional

from fastapi import APIRouter, Query, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from core.dependencies import get_db
from schemas.user import UserSignupRequest
from services.gemini_api import process_user_input
from fastapi import Depends
from services.user_service import user_signup_service

router = APIRouter()

# @router.post("/user/input")
# def prompt_input(
#     aiwi_id: Optional[int] = None,
#     user_id: Optional[int] = None,
#     query: str = Query(..., description="검색어"),
#     db: Session = Depends(get_db),
# ):
#     try:
#         result = process_user_input(query=query, aiwi_id=aiwi_id, user_id=user_id, db=db)
#
#         if "error" in result:
#             return JSONResponse(status_code=500, content=result)
#
#         return JSONResponse(status_code=200, content={
#             "status": "ok",
#             "aiwi_id": result["aiwi_id"],
#             "final_result": result["final_result"]
#         })
#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
@router.post("/user/signup")
def user_signup(
        request: UserSignupRequest,
        db: Session = Depends(get_db)
):

    try:
        user_signup_service(
            email= request.email,
            password= request.password,
            nickname= request.nickname,
            age= request.age,
            sex = request.sex,
            db=db
        )
        return JSONResponse(status_code=200, content={"status": "ok"})
    except HTTPException as he:
        raise he

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


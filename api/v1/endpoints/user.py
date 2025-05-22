from typing import Optional

from fastapi import APIRouter, Query, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from core.dependencies import get_db
from schemas.user import UserSignupRequest, UserInputRequest
from services.gemini_api import process_user_input
from fastapi import Depends
from services.user_service import user_signup_service

router = APIRouter()

@router.post("/user/input")
def prompt_input(
    request: UserInputRequest,
    db: Session = Depends(get_db)
):
    try:
        result = process_user_input(query=request.query, aiwi_id=request.aiwi_id, user_id=request.user_id, db=db)

        if "error" in result:
            return JSONResponse(status_code=500, content=result)

        return JSONResponse(status_code=200, content={
            "status": "ok",
            "chat_id": result["chat_id"],
            "final_result": result["final_result"]
        })
    except Exception as e:
        response_data = {
            "error발생!!": str(e),
            "result": result  # result 전체를 error 정보와 함께 보냄
        }
        return JSONResponse(status_code=500, content=response_data)

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


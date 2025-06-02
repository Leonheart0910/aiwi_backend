from fastapi import APIRouter, Query, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from core.dependencies import get_db
from schemas.user import UserSignupRequest, UserInputRequest, UserLoginRequest, UserWithDrawRequest
from services.gemini_api import process_user_input
from fastapi import Depends
from services.user_service import user_signup_service, user_login_service, user_withdraw_service, user_information_service

router = APIRouter()

@router.post("/user/input")
def prompt_input(
    request: UserInputRequest,
    db: Session = Depends(get_db)
):
    result = process_user_input(query=request.query, aiwi_id=request.aiwi_id, user_id=request.user_id, db=db)

    if "error" in result:
        return JSONResponse(status_code=500, content=result)

    return JSONResponse(status_code=200, content={
        "status": "ok",
        "chat_id": result["chat_id"],
        "final_result": result["final_result"]
    })


@router.post("/user/login")
def user_login(
        request: UserLoginRequest,
        db: Session = Depends(get_db)
):
    user = user_login_service(request.email, request.password, db=db)
    return JSONResponse(status_code=200, content={
        "status": "ok",
        "user_id": user["user_id"],
        "email": user["email"],
        "nickname": user["nickname"]
    })

@router.post("/user/signup")
def user_signup(
        request: UserSignupRequest,
        db: Session = Depends(get_db)
):
    user_signup_service(
        email= request.email,
        password= request.password,
        nickname= request.nickname,
        age= request.age,
        sex = request.sex,
        db=db
    )
    return JSONResponse(status_code=200, content={"status": "ok"})

@router.delete("/user/withdraw")
def user_withdraw(
        request: UserWithDrawRequest,
        db: Session = Depends(get_db)
):

    response =user_withdraw_service(
        user_id = request.user_id,
        db=db)
    return response

@router.get("/user/{user_id}")
def user_information(user_id: int,
                     db : Session = Depends(get_db)):
    response = user_information_service(
        user_id = user_id,
        db=db)
    return response


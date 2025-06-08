from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.dto_builder.chat_response_builder import build_chat_response
from core.dependencies import get_db
from services.chat_service import chat_input_service, chat_list_service

router = APIRouter()


@router.get("/chat/{chat_id}/{user_id}/{user_input}")
def chat_input(
        chat_id: str,
        user_input: str,
        user_id: int,
        db: Session = Depends(get_db)
):
    return chat_input_service(chat_id=chat_id,
                                  user_input=user_input,
                                  user_id=user_id,
                                  db=db)
@router.get("/chat/{chat_id}")
def chat_history(
        chat_id: str,
        db: Session = Depends(get_db)
):
    return build_chat_response(chat_id=chat_id, db = db)

@router.get("/chat/user/{user_id}")
def chat_list(
        user_id: int,
        db: Session = Depends(get_db)
):
    return chat_list_service(user_id=user_id,
                             db=db)



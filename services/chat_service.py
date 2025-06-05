from sqlalchemy.orm import Session, load_only
from sqlalchemy.sql.sqltypes import NULLTYPE

from api.dto_builder.chat_log_response_builder import build_chat_log_response
from constant.message.error_message import ErrorMessage
from core.aiwi import generate_checklist, search_naver_items, compare_and_recommend
from crud.chat import create_chat
from crud.chat_log import create_chat_log
from exception.exception import OperatedException, ErrorCode
from models.aiwi import Aiwi
from schemas.chat_response import ChatOut


def chat_input_service(
        chat_id: int,
        user_input: str,
        user_id: int,
        db: Session
) -> ChatOut:
    try:
        # 1) LLM · 검색 · 추천
        node1_resp = generate_checklist(user_input)
        node2_resp = search_naver_items(node1_resp.checklist_message)
        node4_resp = compare_and_recommend(node2_resp["search_results"])

        # 2) INSERT & 새 log_id 확보
        if chat_id == NULLTYPE:
            chat = create_chat(
                user_id=user_id,
                node1_response=node1_resp,
                node2_response=node2_resp,
                node4_response=node4_resp,
                db=db
            )
            chat_id = chat.chat_id
            new_log_id = chat.chat_logs[0].chat_log_id   # create_chat 내부에서 로그 1개 생성된다고 가정
        else:
            kw_temp = [k["keyword"] for k in node1_resp.keywords]
            kw_full = node1_resp.checklist_message + "\n" + ", ".join(kw_temp)

            new_log = create_chat_log(
                user_input=user_input,
                chat_id=chat_id,
                keyword_full_text=kw_full,
                node1_response=node1_resp,
                node2_response=node2_resp,
                node4_response=node4_resp,
                db=db
            )
            new_log_id = new_log.chat_log_id

        # 3) DTO 만들기 ─ log 1개만
        log_dto = build_chat_log_response(new_log_id, db)

        # 4) 채팅방 메타만 슬림하게 조회
        chat_meta = (
            db.query(Aiwi)
            .options(load_only(Aiwi.title, Aiwi.created_at, Aiwi.updated_at))
            .filter(Aiwi.chat_id == chat_id)
            .one()
        )

        return ChatOut(
            chat_id=chat_id,
            title=chat_meta.title,
            chat_log=[log_dto],
            created_at=chat_meta.created_at,
            updated_at=chat_meta.updated_at,
        )

    except OperatedException:
        raise OperatedException(
            status_code=500,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value,
            detail=ErrorMessage.INTERNAL_SERVER_ERROR.value
        )

def chat_list_service(
        user_id: int,
        db: Session):
    chats = (
        db.query(Aiwi)
        .options(load_only(Aiwi.chat_id, Aiwi.title, Aiwi.updated_at))
        .filter(Aiwi.user_id == user_id)
        .order_by(Aiwi.updated_at.desc())
        .all()
    )
    return chats

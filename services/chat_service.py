from http.client import HTTPException

from sqlalchemy.orm import Session, load_only
from api.dto_builder.chat_log_response_builder import build_chat_log_response
from core.aiwi import generate_checklist, search_naver_items, compare_and_recommend
from crud.chat import create_chat, chat_exist
from crud.chat_log import create_chat_log
from models.aiwi import Aiwi
from schemas.chat_list import ChatList
from schemas.chat_response import ChatOut


def chat_input_service(
        chat_id: str,
        user_input: str,
        user_id: int,
        db: Session
) -> ChatOut:
    try:
        node1_resp = generate_checklist({"question": user_input})
        node2_resp = search_naver_items({
            "question": user_input,
            "checklist_message": node1_resp["checklist_message"],
            "checklist": node1_resp["checklist"],
            "keywords": node1_resp["keywords"]
        })
        node4_resp = compare_and_recommend({
            "keywords": node1_resp["keywords"],
            "search_results": node2_resp["search_results"]
        })

        if chat_exist(chat_id =chat_id, db = db) is False:
            chat = create_chat(
                user_id=user_id,
                chat_id=chat_id,
                node1_response=node1_resp,
                node2_response=node2_resp,
                node4_response=node4_resp,
                db=db
            )
            chat_id = chat.chat_id
            new_log_id = chat.chat_log[0].chat_log_id
        else:
            kw_temp = [k["keyword"] for k in node1_resp["keywords"]]
            kw_full = node1_resp["checklist_message"] + "\n" + ", ".join(kw_temp)

            new_log = create_chat_log(
                user_input=user_input,
                chat_id=chat_id,
                keyword_full_text=kw_full,
                node1_response=node1_resp,
                node2_response=node2_resp,
                node4_response=node4_resp,
                db=db,
                keyword_temp = kw_temp
            )
            new_log_id = new_log.chat_log_id

        # 3) DTO 만들기 ─ log 1개만
        log_dto = build_chat_log_response(new_log_id, db)

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

    except Exception as e:
        raise HTTPException(500, str(e))

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
    return [ChatList(chat_id=c.chat_id, title=c.title, updated_at=c.updated_at) for c in chats]


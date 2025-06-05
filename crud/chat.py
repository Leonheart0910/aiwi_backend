from sqlalchemy.orm import Session

from crud.ai_keyword import create_ai_keyword
from crud.ai_product import create_ai_product
from crud.ai_recommend import create_ai_recommend
from crud.ai_seo_keyword import create_ai_seo_keyword
from crud.chat_log import create_chat_log
from crud.images import create_images
from crud.product import product_exists, create_product
from crud.product_info import create_product_info
from models import Aiwi
from models.chat_log import ChatLog
from schemas.chat import Node1Output, Node2Output, Node4Output


def create_chat(
    user_id: int,
    node1_response: Node1Output,
    node2_response: Node2Output,
    node4_response: Node4Output,
    db: Session
):
    try:
        # 1. Aiwi 생성
        chat = Aiwi(
            title=node1_response.question,
            user_id=user_id,
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)

        # 2. 키워드 전체 텍스트 구성
        keyword_temp = [k["keyword"] for k in node1_response.keywords]
        keyword_full_text = node1_response.checklist_message + "\n" + ", ".join(keyword_temp)

        # 3. chat_log 생성
        chat_log = create_chat_log(
            user_input=node1_response.question,
            chat_id=chat.chat_id,
            keyword_full_text=keyword_full_text,
            node1_response=node1_response,
            node2_response=node2_response,
            node4_response=node4_response,
            db=db,
        )

        return chat

    except Exception as e:
        db.rollback()
        raise e

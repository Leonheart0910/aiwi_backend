from sqlalchemy.orm import Session
from crud.chat_log import create_chat_log
from models import Aiwi
from schemas.chat import Node1Output, Node2Output, Node4Output


def create_chat(
    user_id: int,
    node1_response: Node1Output,
    node2_response: Node2Output,
    node4_response: Node4Output,
    db: Session
):
    try:
        chat = Aiwi(
            title = node1_response["question"],
            user_id=user_id,
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)

        keyword_temp = [k["keyword"] for k in node1_response["keywords"]]

        keyword_full_text = node1_response["checklist_message"] + "\n" + ", ".join(keyword_temp)

        chat_log = create_chat_log(
            user_input=node1_response.question,
            chat_id=chat.chat_id,
            keyword_full_text=keyword_full_text,
            node1_response=node1_response,
            node2_response=node2_response,
            node4_response=node4_response,
            keyword_temp=keyword_temp,
            db=db,
        )

        return chat
    except Exception as e:
        raise e

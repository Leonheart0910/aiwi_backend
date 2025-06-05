from sqlalchemy.orm import Session

from models.ai_keyword import AiKeyword


def create_ai_keyword(
        db: Session,
        chat_log_id: int,
        keyword: str,
        rank: int
):
    ai_keyword = AiKeyword(
        chat_log_id= chat_log_id,
        keyword=keyword,
        rank=rank
    )
    db.add(ai_keyword)
    db.commit()
    db.refresh(ai_keyword)

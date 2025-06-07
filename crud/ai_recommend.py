from sqlalchemy.orm import Session

from models.ai_recommend import AiRecommend


def create_ai_recommend(
        db:Session,
        chat_log_id: int,
        recommend_text: str,
        rank: int
):
    ai_recommend = AiRecommend(
        chat_log_id=chat_log_id,
        recommend_text=recommend_text,
        rank=rank
    )
    db.add(ai_recommend)
    db.commit()
    db.refresh(ai_recommend)
    return ai_recommend
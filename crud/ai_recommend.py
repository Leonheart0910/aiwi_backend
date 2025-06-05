from sqlalchemy.orm import Session

from models.ai_recommend import AiRecommend


def create_ai_recommend(
        db:Session,
        chat_log_id: int,
        recommend: str,
        rank: int
):
    ai_recommend = AiRecommend(
        chat_log_id=chat_log_id,
        recommend=recommend,
        rank=rank
    )
    db.add(ai_recommend)
    db.commit()
    db.refresh(ai_recommend)
    return ai_recommend
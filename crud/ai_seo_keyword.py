from sqlalchemy.orm import Session

from models.ai_seo_keyword import AiSeoKeyword


def create_ai_seo_keyword(
        chat_log_id: int,
        seo_keyword: str,
        rank: int,
        db: Session
):
    ai_seo_keyword = AiSeoKeyword(
        chat_log_id = chat_log_id,
        seo_keyword=seo_keyword,
        rank = rank
    )
    db.add(ai_seo_keyword)
    db.commit()
    db.refresh(ai_seo_keyword)
    return ai_seo_keyword
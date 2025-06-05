from decimal import Decimal

from sqlalchemy.orm import Session

from models.ai_product import AiProduct


def create_ai_product(
        db: Session,
        ai_keyword_id: int,
        product_id: int,
        rank: Decimal,
):
    ai_product = AiProduct(
        ai_keyword_id=ai_keyword_id,
        product_id=product_id,
        rank=rank,
    )
    db.add(ai_product)
    db.commit()
    db.refresh(ai_product)
    return ai_product
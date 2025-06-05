from sqlalchemy.orm import Session

from models.product_info import ProductInfo


def create_product_info(
        db: Session,
        product_id: int,
        product_name: str,
        product_link: str,
        product_price: float
):
    product_info = ProductInfo(
        product_id=product_id,
        product_name=product_name,
        product_link=product_link,
        product_price=product_price
    )

    db.add(product_info)
    db.commit()
    db.refresh(product_info)

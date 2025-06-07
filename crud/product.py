from sqlalchemy.orm import Session

from models.product import Product


def create_product(
        db: Session,
        product_id: int
):
    product = Product(
        product_id = product_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def product_exists(product_id: int,
                   db: Session
                   ) -> bool:
    return db.query(Product).filter(Product.product_id == product_id).first() is not None

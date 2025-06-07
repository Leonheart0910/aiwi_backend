# api/dto_builder/chat_log_response_builder.py
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from models.chat_log import ChatLog
from models.ai_keyword import AiKeyword
from models.ai_product import AiProduct
from models.product import Product
from models.image import Image
from schemas.chat_response import ChatLogOut, ProductOut, ImageOut, RecommendOut


def build_chat_log_response(chat_log_id: int, db: Session) -> ChatLogOut:
    """
    chat_log_id 하나만 ChatLogOut(단일) 구조로 변환
    """
    log: Optional[ChatLog] = (
        db.query(ChatLog)
        .options(
            selectinload(ChatLog.ai_keyword)
            .selectinload(AiKeyword.ai_product)
            .selectinload(AiProduct.product)
            .selectinload(Product.image),

            selectinload(ChatLog.ai_recommend),
            selectinload(ChatLog.ai_seo_keyword),
        )
        .filter(ChatLog.chat_log_id == chat_log_id)
        .one_or_none()
    )

    if log is None:
        raise ValueError(f"chat_log_id {chat_log_id} not found")

    # --- 상품 모으기 ---
    products: list[ProductOut] = []
    for k in log.ai_keyword:
        for ap in k.ai_product:
            p = ap.product
            img: Image | None = p.image[0] if p.image else None
            info = p.product_info[0] if p.product_info else None

            products.append(
                ProductOut(
                    product_id=p.product_id,
                    product_name=info.product_name if info else "",
                    product_link=info.product_link if info else "",
                    product_price=str(info.product_price) if info else "",
                    rank=float(ap.rank),
                    image=ImageOut(
                        image_id=img.image_id,
                        image_url=img.img_url,
                        created_at=img.created_at,
                        updated_at=img.updated_at,
                    ) if img else None,
                    created_at=p.created_at,
                    updated_at=p.updated_at,
                )
            )

    # --- 추천 문구 ---
    recommends = [
        RecommendOut(
            recommend_id=r.ai_recommend_id,
            recommend_text=r.recommend_text,
            rank=r.rank,
        )
        for r in log.ai_recommend
    ]

    seo_text = ", ".join(sk.seo_keyword for sk in log.ai_seo_keyword)

    return ChatLogOut(
        chat_log_id=log.chat_log_id,
        user_input=log.user_input,
        keyword_text=log.keyword_full_text,
        seo_keyword_text=seo_text,
        products=products,
        recommend=recommends,
        created_at=log.created_at,
        updated_at=log.updated_at,
    )

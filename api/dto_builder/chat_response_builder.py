# chat_response_builder.py
from typing import Optional
from sqlalchemy.orm import Session, selectinload
from models.aiwi import Aiwi
from models.chat_log import ChatLog
from models.ai_keyword import AiKeyword
from models.ai_product import AiProduct
from models.product import Product
from models.image import Image
from schemas.chat_response import (
    ChatOut, ChatLogOut, ProductOut, ImageOut, RecommendOut
)


def build_chat_response(chat_id: str, db: Session) -> ChatOut:
    chat: Optional[Aiwi] = (
        db.query(Aiwi)
        .options(
            selectinload(Aiwi.chat_log)
            .selectinload(ChatLog.ai_keyword)        # ← 수정 ①
            .selectinload(AiKeyword.ai_product)      # ← 수정 ②
            .selectinload(AiProduct.product)
            .selectinload(Product.image),
            selectinload(Aiwi.chat_log)
            .selectinload(ChatLog.ai_recommend),

            selectinload(Aiwi.chat_log)
            .selectinload(ChatLog.ai_seo_keyword),
        )
        .filter(Aiwi.chat_id == chat_id)
        .one_or_none()
    )

    if chat is None:
        raise ValueError(f"chat_id {chat_id} not found")

    chat_logs: list[ChatLogOut] = []
    for log in chat.chat_log:
        products: list[ProductOut] = []
        for k in log.ai_keyword:                 # ← 수정 ①
            for ap in k.ai_product:              # ← 수정 ②
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

        recommends = [
            RecommendOut(
                recommend_id=r.ai_recommend_id,
                recommend_text=r.recommend_text,
                rank=r.rank,
            )
            for r in log.ai_recommend
        ]

        seo_text = ", ".join(sk.seo_keyword for sk in log.ai_seo_keyword)

        chat_logs.append(
            ChatLogOut(
                chat_log_id=log.chat_log_id,
                user_input=log.user_input,
                keyword_text=log.keyword_full_text,
                seo_keyword_text=seo_text,
                products=products,
                recommend=recommends,
                created_at=log.created_at,
                updated_at=log.updated_at,
            )
        )

    return ChatOut(
        chat_id=chat.chat_id,
        title=chat.title,
        chat_log=chat_logs,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
    )

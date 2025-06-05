from sqlalchemy.orm import Session
from decimal import Decimal

from constant.message.error_message import ErrorMessage
from crud.ai_keyword import create_ai_keyword
from crud.ai_product import create_ai_product
from crud.ai_recommend import create_ai_recommend
from crud.ai_seo_keyword import create_ai_seo_keyword
from crud.images import create_images
from crud.product import create_product, product_exists
from crud.product_info import create_product_info
from exception.exception import OperatedException, ErrorCode
from models.chat_log import ChatLog
from schemas.chat import Node1Output, Node2Output, Node4Output


def create_chat_log(
    user_input: str,
    chat_id: int,
    keyword_full_text: str,
    node1_response: Node1Output,
    node2_response: Node2Output,
    node4_response: Node4Output,
    db: Session,
    keyword_temp=None
):
    try:
        chat_log = ChatLog(
            user_input=user_input,
            chat_id=chat_id,
            keyword_full_text=keyword_full_text
        )
        db.add(chat_log)
        db.commit()
        db.refresh(chat_log)

        for i in range(1, len(node1_response.keywords) + 1):
            ai_keyword = create_ai_keyword(
                chat_log_id=chat_log.chat_log_id,
                keyword=keyword_temp[i - 1],
                rank=i,
                db=db
            )

            plus = Decimal("0.1")

            for group in node2_response.search_results:
                if group["keyword"] == ai_keyword.keyword:
                    for item in group["items"]:
                        try:
                            product_id = int(item["productId"])
                            price = float(item["lprice"])
                        except (ValueError, TypeError):
                            continue  # 건너뜀

                        if product_exists(product_id=product_id, db=db):
                            create_ai_product(
                                ai_keyword_id=ai_keyword.ai_keyword_id,
                                product_id=product_id,
                                rank=float(i) + float(plus)
                            )
                            plus += Decimal("0.1")
                        else:
                            product = create_product(
                                product_id=product_id,
                                db=db
                            )
                            create_product_info(
                                product_id=product.product_id,
                                product_name=item["title"],
                                product_link=item["link"],
                                product_price=price,
                                db=db
                            )
                            create_images(
                                product_id=product.product_id,
                                img_url=item["image"],
                                db=db
                            )

            create_ai_seo_keyword(
                chat_log_id=chat_log.chat_log_id,
                seo_keyword=keyword_temp[i - 1],
                rank=i,
                db=db
            )

            create_ai_recommend(
                chat_log_id=chat_log.chat_log_id,
                recommend=node4_response.recommendations[i - 1].summary,
                rank=i,
                db=db
            )

        return chat_log

    except Exception as e:
        db.rollback()
        raise OperatedException(
            status_code=500,
            error_code=ErrorCode.INTERNAL_SERVER_ERROR.value,
            detail=str(e)
        )

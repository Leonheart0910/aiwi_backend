from sqlalchemy.orm import Session

from models.chat_log import ChatLog
from schemas.aiwi_log import AiwiLogCreate


def create_aiwi_log(db: Session, aiwi_log_create: AiwiLogCreate):

    aiwi_log = ChatLog(
        user_input=aiwi_log_create.user_input,
        ai_output1=aiwi_log_create.ai_output1,
        ai_output2=aiwi_log_create.ai_output2,
        ai_output3=aiwi_log_create.ai_output3,
        chat_id=aiwi_log_create.chat_id,
    )
    db.add(aiwi_log)
    db.commit()
    db.refresh(aiwi_log)
    return aiwi_log


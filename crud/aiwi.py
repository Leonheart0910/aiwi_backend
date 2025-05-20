from sqlalchemy.orm import Session
from models.aiwi import Aiwi
from schemas.aiwi import AiwiCreate

def create_aiwi(db: Session, aiwi_create: AiwiCreate):
    aiwi = Aiwi(
        title=aiwi_create.title,
        user_id=aiwi_create.user_id
    )
    db.add(aiwi)
    db.commit()
    db.refresh(aiwi)
    return aiwi

def get_aiwis_by_user(db : Session, user_id:int):
    return db.query(Aiwi).filter(Aiwi.user_id == user_id).all()

def delete_aiwi(db : Session, chat_id:int):
    aiwi = db.query(Aiwi).filter(Aiwi.chat_id == chat_id).first()
    if aiwi:
        db.delete(aiwi)
        db.commit()
    return aiwi
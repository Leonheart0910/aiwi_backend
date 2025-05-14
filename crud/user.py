from models.user import User
from models.user_info import UserInfo
from schemas.user import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

def create_user(db: Session, user_create: UserCreate):
    user = User(
        email=user_create.email,
        password=user_create.password,
        nickname=user_create.nickname
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_info = UserInfo(
        age=user_create.user_info.age,
        sex=user_create.user_info.sex,
        user_id=user.user_id
    )
    db.add(user_info)
    db.commit()
    db.refresh(user_info)

    return user
def find_user_by_id(db: Session, user_id: int):
    return db.query(User)\
        .options(joinedload(User.user_info))\
        .filter(User.user_id == user_id)\
        .first()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

from schemas.user import UserCreate, UserLoginRequest
from schemas.user_info import UserInfoCreate
from crud.user import create_user
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User
def user_login_service(email: str,
                       password: str,
                       db: Session):
    try:
        existing_user = db.query(User).filter(User.email == email ,
                                              User.password == password).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return {
                "user_id" : existing_user.user_id,
                "email": existing_user.email,
                "nickname": existing_user.nickname
            }
    except Exception as e:
        raise e


def user_signup_service(email: str,
                password: str,
                nickname: str,
                age: int,
                sex: str,
                db: Session):

    try:
        user_data = UserCreate(
            email=email,
            password=password,
            nickname=nickname,
            user_info=UserInfoCreate(age=age, sex=sex)
        )

    #SQLAlchemy모델을 만들어서 DB에 저장한다.
        created_user = create_user(db=db, user_create=user_data)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



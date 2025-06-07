from constant.message.error_message import ErrorMessage
from constant.message.success_message import SuccessMessage
from exception.exception import OperatedException, ErrorCode
from schemas.user import UserCreate, UserInformationResponse
from schemas.user_info import UserInfoCreate, UserInfoOut
from crud.user import create_user, delete_user
from sqlalchemy.orm import Session
from models.user import User

def user_login_service(email: str,
                       password: str,
                       db: Session):
    try:
        existing_user = db.query(User).filter(User.email == email ,
                                              User.password == password).first()
        if not existing_user:
            raise OperatedException(
            status_code=400,
            error_code=ErrorCode.USER_LOGIN_FAIL.value,
            detail=ErrorMessage.USER_LOGIN_FAIL.value
            )
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
    except OperatedException:
        raise OperatedException(
            status_code=400,
            error_code=ErrorCode.USER_SIGNUP_FAIL.value,
            detail=ErrorMessage.USER_SIGNUP_FAIL.value
        )


def user_withdraw_service(user_id: int,
                          db: Session):
    try:
        existing_user = db.query(User).filter(User.user_id == user_id).first()
        if not existing_user:
            raise OperatedException(
                status_code=400,
                error_code=ErrorCode.USER_WITHDRAW_FAIL.value,
                detail= ErrorMessage.USER_WITHDRAW_FAIL.value
            )
        else:
            delete_user(db=db, user_id=user_id)
            return {
                "status" : "ok",
                "message" : SuccessMessage.WITHDRAW_SUCCESS
            }
    except OperatedException:
        raise OperatedException(
            status_code=400,
            error_code=ErrorCode.USER_WITHDRAW_FAIL.value,
            detail= ErrorMessage.USER_WITHDRAW_FAIL.value
        )

def user_information_service(user_id: int,
                             db: Session):
    try:
        existing_user = db.query(User).filter(User.user_id == user_id).first()
        if not existing_user:
            raise OperatedException(
                status_code=404,
                error_code=ErrorCode.USER_NOT_FOUND.value,
                detail=ErrorMessage.USER_NOT_FOUND.value)
        else:
            response = UserInformationResponse(
                user_id=existing_user.user_id,
                email = existing_user.email,
                password = existing_user.password,
                nickname = existing_user.nickname,
                user_info= UserInfoOut(
                    user_info_id=existing_user.user_info.user_info_id,
                    age=existing_user.user_info.age,
                    sex=existing_user.user_info.sex,
                    user_id= existing_user.user_info.user_id,
                    created_at=existing_user.user_info.created_at,
                    updated_at=existing_user.user_info.updated_at,
                ),
                created_at=existing_user.created_at,
                updated_at=existing_user.updated_at,
            )
            return response
    except OperatedException :
        raise OperatedException(
            status_code = 400,
            error_code= ErrorCode.USER_NOT_FOUND.value,
            detail = ErrorMessage.USER_INFORMATION_FAIL.value
        )
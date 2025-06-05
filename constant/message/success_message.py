from enum import Enum


class SuccessMessage(Enum):
        LOGIN_SUCCESS = "로그인에 성공하였습니다."
        SIGNUP_SUCCESS = "회원가입에 성공하였습니다."
        WITHDRAW_SUCCESS = "회원탈퇴가 정상적으로 승인되었습니다."
        COLLECTION_CREATE_SUCCESS = "장바구니 생성에 성공하였습니다."
        COLLECTION_DELETE_SUCCESS = "장바구니 삭제에 성공하였습니다."
        RESPONSE_COLLECTION = "장바구니 반환에 성공하였습니다."
        DELETE_ITEM_IN_COLLECTION = "장바구니 안의 상품을 제거하는데 성공하였습니다."
        USER_LOOKUP_SUCCESS = "유저정보 반환에 성공하였습니다."


from enum import Enum


class ErrorMessage(Enum):
        USER_SIGNUP_FAIL = "회원가입에 실패하였습니다."
        USER_LOGIN_FAIL = "로그인에 실패하였습니다."
        USER_INFORMATION_FAIL = "유저 정보 반환에 실패하였습니다."
        USER_WITHDRAW_FAIL = "회원탈퇴에 실패하였습니다."
        USER_NOT_FOUND = "유저를 찾을 수 없습니다."

        ITEM_NOT_FOUND = "해당하는 상품을 찾을 수 없습니다."
        ITEM_IN_COLLECTION_DELETE_FAIL = "장바구니의 상품을 제거하는데 실패하였습니다."
        ITEM_IN_COLLECTION_INFORMATION_FAIL = "장바구니의 상품을 불러오는데 실패하였습니다."

        EMAIL_INVALID = "이메일이 잘못되었습니다."
        PASSWORD_INVALID = "비밀번호가 잘못되었습니다."
        EMAIL_PASSWORD_INVALID = "이메일 또는 패스워드가 잘못되었습니다."

        COLLECTION_ITEMS_INFORMATION_FAIL = "장바구니의 아이템들을 불러오는데 실패하였습니다."
        COLLECTION_CREATE_FAIL = "장바구니 생성에 실패하였습니다."
        COLLECTION_DELETE_FAIL = "장바구니 삭제에 실패하였습니다."
        COLLECTION_NOT_FOUND = "장바구니를 찾을 수 없습니다."

        INTERNAL_SERVER_ERROR = "오류가 발생했습니다."
from enum import Enum
from fastapi.exceptions import HTTPException

class ErrorCode(Enum):
    # Bad Request
    INVALID_INPUT = 1100
    USER_SIGNUP_FAIL = 1101
    USER_LOGIN_FAIL = 1102
    # Unauthorized
    EMPTY_TOKEN = 2001
    TOKEN_EXPIRED = 2002
    INVALID_TOKEN = 2003
    DENIED_PERMISSION = 2004
    EMAIL_INVALID = 2005
    PASSWORD_INVALID = 2006


    # Not Found
    RESOURCE_NOT_FOUND = 4001
    USER_NOT_FOUND = 4002
    USER_WITHDRAW_FAIL = 4003


    # Internal Server Error
    UNEXPECTED_ERROR = 9000
    CONNECTION_ERROR = 9001
    MODEL_TIMEOUT = 9101


    COLLECTION_NOT_FOUND = 8001
    COLLECTION_ITEMS_INFORMATION_FAIL = 8002
    COLLECTION_CREATE_FAIL = 8003
    ITEM_IN_COLLECTION_DELETE_FAIL = 9002
    ITEM_IN_COLLECTION_INFORMATION_FAIL = 9003

class OperatedException(HTTPException):
    def __init__(self, status_code: int, error_code: ErrorCode, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.code = error_code
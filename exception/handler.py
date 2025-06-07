from fastapi import HTTPException, FastAPI, Request
from fastapi.responses import JSONResponse

from exception.exception import OperatedException, ErrorCode
from enum import Enum

def set_error_handlers(app: FastAPI):

    @app.exception_handler(OperatedException)
    async def operated_exception_handler(request: Request, exc: OperatedException) -> JSONResponse:
        #log_service.insert_client_log(request = request)

        code = exc.code.value if isinstance(exc.code, Enum) else exc.code
        reason = exc.code.name if isinstance(exc.code, Enum) else str(exc.code)
        return JSONResponse(
            status_code=exc.status_code,
            content={"code": code, "reason": reason, "message": exc.detail}
        )
    @app.exception_handler(Exception)
    async def server_side_exception_handler(request: Request, exc: Exception):
        #log_service.insert_service_log(request = request, exception= exc)

        return JSONResponse(
            status_code=500,
            content={"code": ErrorCode.UNEXPECTED_ERROR.value}
        )
        
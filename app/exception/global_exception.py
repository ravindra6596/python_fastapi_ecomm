import traceback

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.response_schema import CustomResponse


async def global_exception_handler(
        request: Request,
        exc: Exception
):
    print("Exception:", str(exc))
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content=CustomResponse.error_response(
            statusCode=500,
            message="Internal Server Error",
            error=str(exc),
            data={}
        )
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=CustomResponse.error_response(
            statusCode=exc.status_code,
            message=exc.detail,
            error=str(exc),
            data={}
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for err in exc.errors():
        field = " -> ".join(map(str, err["loc"]))
        message = err["msg"]
        errors.append(f"{field}: {message}")

    return JSONResponse(
        status_code=422,
        content=CustomResponse.error_response(
            statusCode=422,
            message="Validation Error",
            error=errors,
            data={}
        )
    )
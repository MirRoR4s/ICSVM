from fastapi import FastAPI, Request, status
from pydantic.errors import PydanticUserError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from .errors import BaseExceptionMixin
from app.common.log import logger as log
from app.schemas.response_code import CustomResponse, CustomResponseCode, StandardResponseCode
from app.schemas.response_schema import ResponseModel, response_base
from app.core.conf import settings
from ...schemas.base import (
    CUSTOM_USAGE_ERROR_MESSAGES,
    CUSTOM_VALIDATION_ERROR_MESSAGES,
)


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        全局HTTP异常处理
        """
        content = ResponseModel(code=exc.status_code, msg=exc.detail).model_dump()
        request.state.__request_http_exception__ = content  # 用于在中间件中获取异常信息
        if settings.ENVIRONMENT == 'dev':
            return JSONResponse(content, status.HTTP_400_BAD_REQUEST, exc.headers)
        return await response_base.fail(res=CustomResponseCode.HTTP_400)

    @app.exception_handler(PydanticUserError)
    async def pydantic_user_error_handler(request: Request, exc: PydanticUserError):
        """
        Pydantic 用户异常处理

        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=StandardResponseCode.HTTP_500,
            content=await response_base.fail(
                res=CustomResponse(code=StandardResponseCode.HTTP_500, msg=CUSTOM_USAGE_ERROR_MESSAGES.get(exc.code))
            ),
        )

    @app.exception_handler(AssertionError)
    async def assertion_error_handler(request: Request, exc: AssertionError):
        """
        断言错误处理
        """
        return JSONResponse(
            status_code=StandardResponseCode.HTTP_500,
            content=ResponseModel(
                code=StandardResponseCode.HTTP_500,
                msg=str(''.join(exc.args) if exc.args else exc.__doc__),
            ).model_dump()
            if settings.ENVIRONMENT == 'dev'
            else await response_base.fail(CustomResponseCode.HTTP_500),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局异常处理

        :param request:
        :param exc:
        :return:
        """
        if isinstance(exc, BaseExceptionMixin):
            return JSONResponse(
                status_code=StandardResponseCode.HTTP_400,
                content=ResponseModel(
                    code=exc.code,
                    msg=str(exc.msg),
                    data=exc.data if exc.data else None,
                ).model_dump(),
                background=exc.background,
            )
        else:
            import traceback

            log.error(f'未知异常: {exc}')
            log.error(traceback.format_exc())
            return JSONResponse(
                status_code=StandardResponseCode.HTTP_500,
                content=ResponseModel(code=500, msg=str(exc)).model_dump()
                if settings.ENVIRONMENT == 'dev'
                else await response_base.fail(CustomResponseCode.HTTP_500),
            )

    if settings.MIDDLEWARE_CORS:

        @app.exception_handler(StandardResponseCode.HTTP_500)
        async def cors_status_code_500_exception_handler(request, exc):
            """
            跨域 500 异常处理

            `Related issue <https://github.com/encode/starlette/issues/1175>`_

            :param request:
            :param exc:
            :return:
            """
            if isinstance(exc, BaseExceptionMixin):
                content = ResponseModel(code=exc.code, msg=exc.msg, data=exc.data).model_dump()
            else:
                content = (
                    ResponseModel(code=StandardResponseCode.HTTP_500, msg=str(exc)).model_dump()
                    if settings.ENVIRONMENT == 'dev'
                    else await response_base.fail(CustomResponseCode.HTTP_500)
                )
            response = JSONResponse(
                status_code=exc.code if isinstance(exc, BaseExceptionMixin) else StandardResponseCode.HTTP_500,
                content=content,
                background=exc.background if isinstance(exc, BaseExceptionMixin) else None,
            )
            origin = request.headers.get('origin')
            if origin:
                cors = CORSMiddleware(
                    app=app,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*'],
                )
                response.headers.update(cors.simple_headers)
                has_cookie = 'cookie' in request.headers
                if cors.allow_all_origins and has_cookie:
                    response.headers['Access-Control-Allow-Origin'] = origin
                elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
                    response.headers['Access-Control-Allow-Origin'] = origin
                    response.headers.add_vary_header('Origin')
            return response

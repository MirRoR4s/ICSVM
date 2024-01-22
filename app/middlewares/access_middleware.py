"""访问日志中间件"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.log import logger as log
from app.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """请求和响应日志中间件"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # 请求日志
        start_time = timezone.now()
        body = await request.body()
        log.info(f"Request: {start_time} {request.method} {request.url} {body}")
        response = await call_next(request)
        # body = b"".join([chunk for chunk in response.__dict__['body_iterator']])
        # end_time = timezone.now()
        # log.info(f'响应状态码：{response.status_code} 响应体：{body} 响应时间：{end_time} 响应用时：{end_time - start_time}')
        return response

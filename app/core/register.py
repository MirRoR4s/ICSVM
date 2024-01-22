"""FastAPI 资源注册"""
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware
from app.api.routers import v1
from ..common.redis import redis_client
from app.core.conf import settings
from app.database.db_mysql import create_table
from app.middlewares.auth_middleware import JWTAuthMiddleware
from app.middlewares.opera_log_middleware import OperaLogMiddleware
from app.utils.demo_site import demo_site
from app.utils.health_check import ensure_unique_route_names, http_limit_callback
from app.utils.openapi import simplify_operation_ids


# 创建异步上下文管理器。
@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # 创建数据库表
    await create_table()
    # 连接 redis
    await redis_client.is_connected()
    # 初始化 limiter
    await FastAPILimiter.init(
        redis_client,
        prefix=settings.LIMITER_REDIS_PREFIX,
        http_callback=http_limit_callback,
    )

    yield

    # 关闭 redis 连接
    await redis_client.close()
    # 关闭 limiter
    await FastAPILimiter.close()


def register_app():
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=register_init,
    )
    # 静态文件
    # register_static_file(app)
    # 中间件
    register_middleware(app)
    print("中间件已加载")
    # 路由
    register_router(app)
    # 分页
    # register_page(app)
    # 全局异常处理
    # register_exception(app)

    return app


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务
    - fastapi 静态文件参看： https://fastapi.tiangolo.com/zh/tutorial/static-files/
    """
    if settings.STATIC_FILES:
        import os
        from fastapi.staticfiles import StaticFiles

        if not os.path.exists("./static"):
            os.mkdir("./static")
        app.mount("/static", StaticFiles(directory="static"), name="static")


def register_middleware(app: FastAPI):
    """
    中间件，执行顺序从下往上
    也就是最后添加的中间件最先执行
    """
    # # Gzip: Always at the top
    # if settings.MIDDLEWARE_GZIP:
    #     from fastapi.middleware.gzip import GZipMiddleware
    #     app.add_middleware(GZipMiddleware)
    # Opera log
    # app.add_middleware(OperaLogMiddleware)

    # JWT auth, required
    # app.add_middleware(
    #     AuthenticationMiddleware,
    #     backend=JWTAuthMiddleware(
    #         settings.TOKEN_SECRET_KEY,
    #         algorithm=settings.TOKEN_ALGORITHM,
    #         excluded_routers=settings.TOKEN_EXCLUDE,
    #     ),
    # )

    # Access log
    if settings.MIDDLEWARE_ACCESS:
        from app.middlewares.access_middleware import AccessMiddleware
        app.add_middleware(AccessMiddleware)

    # CORS: Always at the end
    # 关于 fastapi 跨域资源共享中间件参看 https://fastapi.tiangolo.com/zh/tutorial/cors/
    # if settings.MIDDLEWARE_CORS:
    #     from fastapi.middleware.cors import CORSMiddleware
    #
    #     app.add_middleware(
    #         CORSMiddleware,
    #         allow_origins=["*"],
    #         allow_credentials=True,
    #         allow_methods=["*"],
    #         allow_headers=["*"],
    #     )


def register_router(app: FastAPI):
    dependencies = [Depends(demo_site)] if settings.DEMO_MODE else None
    # API
    app.include_router(v1, dependencies=dependencies)
    # 确保路由名称唯一
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI):
    """
    分页查询
    """
    add_pagination(app)

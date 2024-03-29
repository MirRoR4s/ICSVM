"""
全局配置文件
"""
from functools import lru_cache
from typing import Literal
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


# 获取当前文件的绝对路径
current_path = os.path.abspath(__file__)
# 获取项目的根目录
root_path = os.path.dirname(os.path.dirname(current_path))
# 设置.env文件的路径，注意 .env 文件的路径是相对于运行 uvicorn 的目录的，而不是项目根目录
ENV_FILE_PATH = os.path.join(root_path, '.env')

class Settings(BaseSettings):
    """TODO"""
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding='utf-8')

    # Env Config
    # ENVIRONMENT的值只能是'dev'或者'pro'
    ENVIRONMENT: Literal['dev', 'pro']

    # Env MySQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    # Env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # Env Celery
    CELERY_REDIS_HOST: str
    CELERY_REDIS_PORT: int
    CELERY_REDIS_PASSWORD: str
    CELERY_BROKER_REDIS_DATABASE: int  # 仅当使用 redis 作为 broker 时生效, 更适用于测试环境
    CELERY_BACKEND_REDIS_DATABASE: int

    # Env Rabbitmq
    # docker run -d --hostname fba-mq --name fba-mq  -p 5672:5672 -p 15672:15672 rabbitmq:latest
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str

    # Env Token
    TOKEN_SECRET_KEY: str  # 密钥 secrets.token_urlsafe(32)

    # Env Opera Log
    OPERA_LOG_ENCRYPT_SECRET_KEY: str  # 密钥 os.urandom(32), 需使用 bytes.hex() 方法转换为 str

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = 'FastAPI'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPI Best Architecture'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    OPENAPI_URL: str | None = f'{API_V1_STR}/openapi'

    @model_validator(mode='before')
    @classmethod
    def validate_openapi_url(cls, values):
        """
        _summary_

        :param values: _description_
        :return: _description_
        """
        value = values.get('ENVIRONMENT')
        if value == 'pro':
            values['OPENAPI_URL'] = None
        return values

    # Demo mode
    # Only GET, OPTIONS requests are allowed
    DEMO_MODE: bool = False
    DEMO_MODE_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{API_V1_STR}/auth/login'),
        ('POST', f'{API_V1_STR}/auth/logout'),
        ('GET', f'{API_V1_STR}/auth/captcha'),
    }

    # Uvicorn
    UVICORN_HOST: str = '127.0.0.1'
    UVICORN_PORT: int = 8000
    UVICORN_RELOAD: bool = True

    # Static Server
    STATIC_FILES: bool = False

    # Location Parse
    LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'

    # Limiter
    LIMITER_REDIS_PREFIX: str = 'fba_limiter'

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # MySQL
    DB_ECHO: bool = False
    DB_DATABASE: str = 'fba'
    DB_CHARSET: str = 'utf8mb4'

    # Redis
    REDIS_TIMEOUT: int = 5

    # Token
    TOKEN_ALGORITHM: str = 'HS256'  # 算法
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # 过期时间，单位：秒
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 刷新过期时间，单位：秒
    TOKEN_URL_SWAGGER: str = f'{API_V1_STR}/auth/swagger_login'
    TOKEN_REDIS_PREFIX: str = 'fba_token'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'fba_refresh_token'
    TOKEN_EXCLUDE: list[str] = [  # 白名单
        f'{API_V1_STR}/openapi',
        f'{API_V1_STR}/auth/login',
        f'{API_V1_STR}/auth/swagger_login'
    ]

    # Captcha
    CAPTCHA_LOGIN_REDIS_PREFIX: str = 'fba_login_captcha'
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5  # 过期时间，单位：秒

    # Log
    LOG_STDOUT_FILENAME: str = 'fba_access.log'
    LOG_STDERR_FILENAME: str = 'fba_error.log'

    # Middleware
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_GZIP: bool = True
    MIDDLEWARE_ACCESS: bool = True

    # Casbin
    CASBIN_RBAC_MODEL_NAME: str = 'rbac_model.conf'
    CASBIN_EXCLUDE: set[tuple[str, str]] = {
        ('POST', f'{API_V1_STR}/auth/swagger_login'),
        ('POST', f'{API_V1_STR}/auth/login'),
        ('POST', f'{API_V1_STR}/auth/logout'),
        ('POST', f'{API_V1_STR}/auth/register'),
        ('GET', f'{API_V1_STR}/auth/captcha'),
    }

    # Menu
    MENU_PERMISSION: bool = False  # 危险行为，开启此功能, Casbin 鉴权将失效，并将使用角色菜单鉴权 (默认关闭)
    MENU_EXCLUDE: list[str] = [
        'auth:swagger_login:post',
        'auth:login:post',
        'auth:logout:post',
        'auth:register:post',
        'auth:captcha:get',
    ]

    # Opera log
    OPERA_LOG_EXCLUDE: list[str] = [
        '/favicon.ico',
        DOCS_URL,
        REDOCS_URL,
        OPENAPI_URL,
        f'{API_V1_STR}/auth/swagger_login',
    ]
    OPERA_LOG_ENCRYPT: int = 1  # 0: AES (性能损耗); 1: md5; 2: ItsDangerous; 3: 不加密, others: 替换为 ******
    OPERA_LOG_ENCRYPT_INCLUDE: list[str] = [
        'password',
        'old_password',
        'new_password',
        'confirm_password',
    ]

    # Ip location
    IP_LOCATION_REDIS_PREFIX: str = 'fba_ip_location'
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # 过期时间，单位：秒

    # Celery
    CELERY_BROKER: Literal['rabbitmq', 'redis'] = 'redis'
    CELERY_BACKEND_REDIS_PREFIX: str = 'fba_celery'
    CELERY_BACKEND_REDIS_TIMEOUT: float = 5.0
    CELERY_BACKEND_REDIS_ORDERED: bool = True
    CELERY_BEAT_SCHEDULE_FILENAME: str = './log/celery_beat-schedule'
    CELERY_BEAT_SCHEDULE: dict = {
        'task_demo_async': {
            'task': 'tasks.task_demo_async',
            'schedule': 5.0,
        },
    }

    @model_validator(mode='before')
    def validate_celery_broker(cls, values):
        value = values.get('ENVIRONMENT')
        if value == 'pro':
            values['CELERY_BROKER'] = 'rabbitmq'
        return values


@lru_cache
def get_settings():
    """读取配置优化"""
    return Settings()


settings = get_settings()

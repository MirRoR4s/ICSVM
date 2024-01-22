"""
Redis 客户类，负责从 Redis 服务器中查询和插入 token
"""
import sys
from redis.asyncio.client import Redis
from redis.exceptions import AuthorizationError, TimeoutError
from app.common.log import logger as log
from app.core.conf import settings


class RedisClient(Redis):
    """
    Redis 客户类，负责从 Redis 服务器中查询和插入 token
    """
    def __init__(self):
        super(RedisClient, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,  # 自动将从Redis服务器接收到的响应解码为字符串 utf-8。
        )

    async def is_connected(self) -> None:
        """
        检测和 Redis 服务器的连接情况
        """
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ 数据库 redis 连接超时')
            sys.exit()
        except AuthorizationError:
            log.error('❌ 数据库 redis 连接认证失败')
        except Exception as e:
            log.error('❌ 数据库 redis 连接异常 {}', e)
            raise

    async def delete_prefix(self, prefix: str, exclude: str | list = None):
        """
        删除指定 prefix 并且不在 exclude 参数中的所有键。

        :param prefix: 要删除的key的前缀
        :param exclude: 要排除的key，可以是单个字符串或字符串列表，默认为None
        :return: None
        """
        keys = []
        # 迭代所有匹配 prefix 前缀的 key
        async for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                keys.append(key) if key != exclude else None
            elif isinstance(exclude, list):
                keys.append(key) if key not in exclude else None
            else:
                keys.append(key)
        for key in keys:
            await self.delete(key)


redis_client = RedisClient()





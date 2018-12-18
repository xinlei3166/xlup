#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import aioredis
from sanic.log import logger


class Cache:
    """redis操作方法封装"""

    def __init__(self, loop, cache):
        self._loop = loop
        self._cache = cache

    async def set(self, *args, **kwargs):
        """redis set 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            await redis.set(*args, **kwargs)

    async def get(self, *args, **kwargs):
        """redis get 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.get(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        """redis del 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            await redis.delete(*args, **kwargs)

    async def lpush(self, *args, **kwargs):
        """redis lpush 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            await redis.lpush(*args, **kwargs)

    async def lpop(self, *args, **kwargs):
        """redis lpop 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.lpop(*args, **kwargs)

    async def rpush(self, *args, **kwargs):
        """redis rpush 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            await redis.rpush(*args, **kwargs)

    async def rpop(self, *args, **kwargs):
        """redis rpop 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.rpop(*args, **kwargs)

    async def hset(self, *args, **kwargs):
        """redis hset 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            await redis.hset(*args, **kwargs)

    async def hget(self, *args, **kwargs):
        """redis hget 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.hget(*args, **kwargs)

    async def hdel(self, *args, **kwargs):
        """redis hdel 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.hdel(*args, **kwargs)

    async def setbit(self, *args, **kwargs):
        """redis setbit 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.setbit(*args, **kwargs)

    async def bitcount(self, *args, **kwargs):
        """redis bitcount 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.bitcount(*args, **kwargs)

    async def pipeline(self, *args, **kwargs):
        """redis pipeline 命令封装"""
        with await aioredis.commands.Redis(self.reids_pool) as redis:
            return await redis.pipeline(*args, **kwargs)

    def __await__(self):
        return self._async_init().__await__()

    async def _async_init(self):
        """定义redis连接池"""
        logger.info('create redis connection pool...')
        self.reids_pool = await aioredis.create_pool(address=self._cache['address'], db=self._cache['db'],
                                                     password=self._cache['password'],
                                                     minsize=self._cache['minsize'], maxsize=self._cache['maxsize'],
                                                     loop=self._loop)
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.reids_pool.close()
        await self.reids_pool.wait_closed()

#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import aiomysql
from sanic.log import logger

# def log(sql, args=()):
#     logger.info('SQL: %s' % sql, *args)


def log(sql):
    logger.info('SQL: %s' % sql)


class PyMySQL:
    """mysql操作方法封装"""

    def __init__(self, loop, database):
        self._loop = loop
        self._database = database

    async def get(self, sql, args=()):
        """封装select，查询单个，返回数据为字典"""
        log(sql)
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                rs = await cur.fetchone()
                return rs

    async def query(self, sql, args=(), size=None):
        """封装select，查询多个，返回数据为列表"""
        log(sql)
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql, args)
                if size:
                    rs = await cur.fetchmany(size)
                else:
                    rs = await cur.fetchall()
                logger.info('rows returned: %s' % len(rs))
                return rs

    async def create(self, sql, args=()):
        """封装insert，并得到单条数据id"""
        return await self._execute_and_get_id(sql, args)

    async def createmany(self, sql, args=()):
        """封装insert批量插入，并得到受影响的行数"""
        return await self._execute_many_and_get_row(sql, args)

    async def update(self, sql, args=()):
        """封装update，并得到受影响的行数"""
        return await self._execute_and_get_row(sql, args)

    async def delete(self, sql, args=()):
        """封装delete，并得到受影响的行数"""
        return await self._execute_and_get_row(sql, args)

    async def _execute_and_get_id(self, sql, args=()):
        """执行单条sql得到单条数据的id"""
        log(sql)
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, args)
                except BaseException as exc:
                    print(exc)
                    await conn.rollback()
                    return
                else:
                    lastrowid = cur.lastrowid
                    return lastrowid

    async def _execute_and_get_row(self, sql, args=()):
        """执行单条sql得到受影响的行数"""
        log(sql)
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, args)
                except BaseException as e:
                    print(e)
                    await conn.rollback()
                    return
                else:
                    affected = cur.rowcount
                    return affected

    async def _execute_many_and_get_row(self, sql, args=()):
        """执行批量操作得到受影响的行数"""
        log(sql)
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.executemany(sql, args)
                except BaseException:
                    await conn.rollback()
                    return
                else:
                    affected = cur.rowcount
                    return affected

    def __await__(self):
        return self._async_init().__await__()

    async def _async_init(self):
        """定义mysql连接池"""
        logger.info('create database connection pool...')
        self.mysql_pool = await aiomysql.create_pool(host=self._database['host'], port=self._database['port'], user=self._database['user'],
            password=self._database['password'], db=self._database['db'], loop=self._loop,
            charset=self._database['charset'], autocommit=self._database['autocommit'],
            maxsize=self._database['maxsize'], minsize=self._database['minsize'])
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.mysql_pool.close()
        await self.mysql_pool.wait_closed()

#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import json
from functools import wraps
from sanic import response
from utils.token import token
from utils.base import hashid_decode
from jwt.exceptions import InvalidTokenError, ExpiredSignature


def check_token(coro):
    """检测token是否合法"""
    @wraps(coro)
    async def inner(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')
        if not access_token:
            return response.json({'code': 'InvalidParams', 'msg': 'missing access_token'})
        if not re.match(r'^Bearer ', access_token):
            return response.json({'code': 'TokenFormatError', 'msg': 'access_token format error'})
        access_token = access_token.split()[1]
        revoke_access_token = await request.app.cache.get('access_token_{}'.format(access_token))
        if revoke_access_token:
            return response.json({'code': 'TokenRevoke', 'msg': 'token revoke'})
        key = request.app.config.auth_key
        try:
            payload = token.decode(key, access_token)
        except ExpiredSignature:
            return response.json({'code': 'AccessTokenExpires', 'msg': 'access_token expires'})
        except InvalidTokenError:
            return response.json({'code': 'InvalidAccessToken', 'msg': 'invalid access_token'})
        token_type = payload.get('token_type')
        if token_type != 'access_token':
            return response.json({'code': 'InvalidTokenType', 'msg': 'invalid token type'})
        user_id = hashid_decode(request.app.config.HASH_KEY, payload.get('sub'))
        user = await request.app.db.get("select id from user where id = %s;", (user_id,))
        if not user:
            return response.json({'code': 'InvalidTokenSub', 'msg': 'invalid access_token sub'})
        return await coro(self, request, user_id=user_id, role=payload.get('role'), *args, **kwargs)
    return inner


def check_permission(permission=None):
    """检查权限"""
    def outer(coro):
        @wraps(coro)
        @check_token
        async def inner(self, request, *args, **kwargs):
            # permissions = kwargs.get('scopes')
            # if permission not in permissions:
            role = kwargs.get('role')
            if role != 'admin':
                return response.json({'code': 'PermissionDenied', 'msg': 'permission denied'})
            return await coro(self, request, *args, **kwargs)
        return inner
    return outer


def cache(*, expire=None):
    """缓存数据"""
    def outer(coro):
        @wraps(coro)
        async def inner(self, request, *args, **kwargs):
            cache_key = kwargs.get('cache_key')
            cache_data = await request.app.cache.get(cache_key)
            if not cache_data:
                data = await coro(self, request, expire=expire, *args, **kwargs)
            else:
                data = json.loads(cache_data)
            return data
        return inner
    return outer

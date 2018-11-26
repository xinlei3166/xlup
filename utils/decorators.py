#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import json
from functools import wraps
from sanic import response
from utils.token import token
from utils.base import hashid_decode
from utils.access_key import get_access_key_secret, generate_policy_sign
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


def check_access_sign(coro):
    """检测access_sign是否合法"""
    @wraps(coro)
    async def inner(self, request, *args, **kwargs):
        access_key_id = request.form.get('access_key_id')
        policy = request.form.get('policy')
        sign = request.form.get('sign')
        if not all([access_key_id, policy, sign]):
            return response.json({'code': 'InvalidParams', 'msg': 'missing access_key_id or policy or sign'})
        access_key_secret = await get_access_key_secret(request.app.db, access_key_id)
        if not access_key_secret:
            return response.json({'code': 'AccessKeyNotExist', 'msg': 'access key not exist'})
        if sign != generate_policy_sign(access_key_secret, policy):
            return response.json({'code': 'InvalidSign', 'msg': 'invalid sign'})
        user = await request.app.db.get("select u.id from user u join access_key a on u.id = a.user_id where a.access_key_id = %s", (access_key_id,))
        if not user:
            return response.json({'code': 'UserNotExist', 'msg': 'user not exist'})
        return await coro(self, request, access_key_id=access_key_id, policy=policy, user_id=user['id'], *args, **kwargs)
    return inner


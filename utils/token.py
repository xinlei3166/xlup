#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import jwt
import time
import shortuuid
from jwt.exceptions import InvalidTokenError


class JWT:
    """JSON Web Token

    usages:
        web_token = JWT()
        token = web_token.encode(key=web_token.key, sub='111', expires_in=2)
        payload = web_token.decode(key=web_token.key, token=token)
        access_token = web_token.generate_access_token(key=web_token.key, sub='111', expires_in=2)
        refresh_token = web_token.generate_refresh_token(key=web_token.key, sub='111', expires_in=20)
        new_access_token = web_token.refresh_access_token(web_token.key, refresh_token)

    eg:
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
    """

    key = '18a01b027e86e93510ffe6abe5fe9b1f'

    @property
    def alg(self):
        """声明加密的算法 通常直接使用 HMAC SHA256"""
        return self._alg

    @property
    def typ(self):
        """声明类型，这里是jwt"""
        return self._typ

    @property
    def jti(self):
        return self.generate_jti()

    @property
    def iss(self):
        return self._iss

    @property
    def iat(self):
        return self.generate_timestamp()

    def __init__(self):
        self._alg = 'HS256'
        self._typ = 'JWT'
        self._iss = 'MGC Online'
        self.access_expires_in = 3600 * 24
        self.refresh_expires_in = 3600 * 24 * 90

    def generate_jti(self):
        return shortuuid.ShortUUID().uuid()

    def generate_timestamp(self):
        return int(time.time())

    def build_payload(self, sub, expires_in, scopes, token_type, aud='client', **kwargs):
        """
        nbf (Not Before)：如果当前时间在nbf里的时间之前，则Token不被接受；一般都会留一些余地，比如几分钟，是否使用是可选的；
        jti: jwt的唯一身份标识，主要用来作为一次性token，从而回避重放攻击。
        iss: 该JWT的签发者，是否使用是可选的。
        sub: 该JWT所面向的用户，是否使用是可选的。
        iat(issued at): 在什么时候签发的(UNIX时间)，是否使用是可选的。
        exp(expires): 什么时候过期，这里是一个Unix时间戳，是否使用是可选的。
        aud: 接收该JWT的一方，是否使用是可选的。
        scopes: 授权域
        """
        payload = {
            'jti': self.jti,
            'iss': self.iss,
            'iat': self.iat,
            # 'exp': self.iat + 3600 * 24 * 7,
            'exp': self.iat + expires_in,
            # 'aud': aud,
            'sub': sub,
            'token_type': token_type,
            'scopes': scopes
        }
        payload.update(kwargs)
        return payload

    def get_unverified_header(self, token):
        return jwt.get_unverified_header(token)

    def encode(self, key, sub, expires_in, scopes=(), token_type='access_token', **kwargs):
        payload = self.build_payload(sub, expires_in, scopes, token_type, **kwargs)
        token = jwt.encode(payload, key, algorithm=self.alg, headers={'typ': self.typ, 'alg': self.alg})
        return token.decode('utf8')

    def decode(self, key, token, verify=True):
        payload = jwt.decode(token, key, algorithms=[self.alg], headers={'typ': self.typ, 'alg': self.alg},
                             verify=verify)
        if payload:
            if self.verify_jti(payload.get('jti')) and self.verify_sub(payload.get('sub')):
                return payload
        return

    def verify_jti(self, jti):
        if jti is None:
            raise InvalidTokenError('invalid jti')
        return True

    def verify_sub(self, sub):
        if sub is None:
            raise InvalidTokenError('invalid sub')
        return True

    def generate_access_token(self, key, sub, expires_in, scopes=(), token_type='access_token', **kwargs):
        return self.encode(key, sub, expires_in, scopes, token_type, **kwargs)

    def generate_refresh_token(self, key, sub, expires_in, scopes=(), token_type='refresh_token', **kwargs):
        return self.encode(key, sub, expires_in, scopes, token_type, **kwargs)

    def refresh_access_token(self, key, refresh_token):
        refresh_payload = self.decode(key, refresh_token)
        access_token = self.generate_access_token(key, refresh_payload.get('sub'), self.access_expires_in,
                                                  scopes=refresh_payload.get('scopes'))
        return access_token


token = JWT()

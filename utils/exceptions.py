#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'


class SysError(Exception):
    """系统错误"""


class APIError(Exception):
    def __init__(self, err_code=None, err_msg=None):
        self.err_code = err_code
        self.err_msg = err_msg

    def __repr__(self):
        return "{}(err_code={},err_msg={})".format(self.__class__.__name__, self.err_code, self.err_msg)


class APIParameterError(APIError):
    """接口参数错误"""


class APIValidationError(APIError):
    """接口参数验证错误"""

#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'


class Paginator:
    """数据分页"""

    def __init__(self, count: int, limit: int):
        self.count = count
        self.limit = limit

    def __call__(self, *args, **kwargs):
        pages = self.count // self.limit
        if pages > 0:
            remain = self.count % self.limit
            if remain > 0:
                pages += 1
        else:
            pages = 1
        return pages


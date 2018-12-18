#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import os

try:
    from .__envir__ import ENVIRONMENT
except ImportError:
    ENVIRONMENT = 'develop'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目路径

HASH_KEY = '95c0e5b348af14522bb880e44e7f2d79'

if ENVIRONMENT == 'production':  # 生产环境
    DATABASE = {
        'engine': 'mysql',
        'db': 'xlup',
        'user': 'xlup',
        'password': '123456',
        'host': 'localhost',
        'port': 3306,
        'charset': 'utf8',
        'minsize': 1,
        'maxsize': 10,
        'autocommit': True
    }

    CACHE = {
        'engine': 'redis',
        'address': ('localhost', 6379),
        'password': None,
        'db': 5,
        'minsize': 1,
        'maxsize': 10
    }

    MEDIA_DIR = '/mnt/xlup'  # 上传文件路径

    UPLOAD_DOMAIN = 'http://uploads.lovecantouch.com'

else:  # 本地环境
    DATABASE = {
        'engine': 'mysql',
        'db': 'xlup',
        'user': 'xlup',
        'password': '123456',
        'host': 'localhost',
        'port': 3306,
        'charset': 'utf8',
        'minsize': 1,
        'maxsize': 10,
        'autocommit': True
    }

    CACHE = {
        'engine': 'redis',
        'address': ('localhost', 6379),
        'password': None,
        'db': 5,
        'minsize': 1,
        'maxsize': 10
    }

    MEDIA_DIR = os.path.join(BASE_DIR, 'uploads')  # 上传文件路径

    UPLOAD_DOMAIN = 'http://localhost:9000'

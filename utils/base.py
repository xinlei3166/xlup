#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import time
import datetime
import decimal
import json
import hashlib
import hmac
from hashids import Hashids


def timestamp_to_strtime(timestamp):
    """时间戳转换为年月日格式时间"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(timestamp)))


class RewriteJsonEncoder(json.JSONEncoder):
    """重写json类，为了解决datetime类型的数据无法被json格式化"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        elif hasattr(obj, 'isoformat'):
            # 处理日期类型
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


def json_dumps(obj):
    return json.dumps(obj, cls=RewriteJsonEncoder)


def hashid_encode(key, _id):
    hashids = Hashids(salt=key, min_length=6)
    hashid = hashids.encode(_id)
    return hashid


def hashid_decode(key, hashid):
    hashids = Hashids(salt=key, min_length=6)
    _id = hashids.decode(hashid)
    return _id[0]


def hash_md5(unencrypted_string):
    """MD5加密"""
    m = hashlib.md5()
    m.update(unencrypted_string.encode('utf-8'))
    return m.hexdigest()


def hmac_sha256(key, unencrypted_string, digestmod=hashlib.sha256):
    """HMAC-SHA256加密"""
    hc = hmac.new(key.encode('utf8'), digestmod=digestmod)
    hc.update(unencrypted_string.encode('utf8'))
    return hc.hexdigest()


def ordered_data(data):
    """字典排序"""
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据dump出来
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))

    return sorted([(k, v) for k, v in data.items()])


def carry_key_hash_md5(key, string):
    """MD5加密，带key"""
    h = hashlib.md5()
    h.update((key + string).encode('utf-8'))
    return h.hexdigest()


def generate_sign(key, data):
    """生成md5签名"""
    items = ordered_data(data)
    string = "&".join("{}={}".format(k, v) for k, v in items)
    return carry_key_hash_md5(key, string)


"""
压缩图片

from PIL import Image
from io import BytesIO


# 定义可以识别的图片文件类型，可以自行扩充
valid_file_type = ['.jpg', '.png']
# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0

infile = 'test.png'

#
# if choose == '1':
#     scale = SIZE_normal
# if choose == '2':
#     scale = SIZE_small
# if choose == '3':
#     scale = SIZE_more_small

scale = 1.0

# img = Image.open(infile)
# w, h = img.size
# img.thumbnail((int(w/scale), int(h/scale)))
# img.save('yasuo_' + infile)


# img = Image.open(infile)
# img.thumbnail((200, 200))
# thumb_io = BytesIO()
# img.save(thumb_io, format='png')
# with open('yasuo_' + infile, 'wb') as f:
#     f.write(thumb_io.getvalue())


with open('test.png', 'rb') as f:
    c = f.read()
img = Image.open(BytesIO(c))
w, h = img.size
img.thumbnail((int(w/scale), int(h/scale)))
img.save('yasuo_' + infile)
img.save('yasuo.jpeg', 'jpeg')
"""

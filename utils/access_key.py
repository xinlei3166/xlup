#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import time
import hmac
import json
import base64
import hashlib
import shortuuid
from utils.base import carry_key_hash_md5


async def get_access_key_secret(db, access_key_id):
    access_key = await db.get("select access_key_secret from access_key where access_key_id = %s", (access_key_id,))
    if access_key:
        return access_key['access_key_secret']


def generate_access_key_id():
    return "MGC{}".format(shortuuid.ShortUUID().random(length=16))


def generate_access_key_secret(key, access_key_id):
    return carry_key_hash_md5(key, access_key_id)


def generate_policy(expires=0, max_content_size=1024 * 1024 * 5, **kwargs):
    policy = dict()
    policy['issued'] = int(time.time())
    policy['expires'] = expires
    policy['max_content_size'] = max_content_size
    policy.update(kwargs)
    return json.dumps(policy)


def convert_base64(json_data):
    return base64.b64encode(json_data.encode('utf-8')).decode('utf-8')


def generate_policy_sign(key, policy):
    base64policy = convert_base64(policy)
    return base64.b64encode(hmac.new(key.encode('utf-8'), base64policy.encode('utf-8'), hashlib.sha1).digest()).decode(
        'utf-8')

# policy = generate_policy()
# print(policy)
# print(generate_policy_sign('51b0c82c5ef9f7e464fa4a1dbc1a21c2', policy))

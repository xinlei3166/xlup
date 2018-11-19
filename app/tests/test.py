#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

"""单元测试
Usages:
    pytest -q test.py
    pytest -q test.py --html=.pytest_cache/report.html
"""

import pytest
from main import app as webserver

# @pytest.yield_fixture
# def app():
#     app = Sanic("test_sanic_app")
#
#     @app.route("/test_get", methods=['GET'])
#     async def test_get(request):
#         return response.json({"GET": True})
#
#     yield app

@pytest.yield_fixture
def app():
    app = webserver
    yield app


@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app))

#########
# Tests #
#########


token = 'Bearer '
token += 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJIaUFxaDMzc1NtemJoV1d3dlBWZTU0IiwiaXNzIjoiTUdDIE9ubGluZSIsImlhdCI6MTU0MjI2OTQyOSwiZXhwIjoxNTQyMzU1ODI5LCJzdWIiOiJ6d000UFgiLCJ0b2tlbl90eXBlIjoiYWNjZXNzX3Rva2VuIiwic2NvcGVzIjpbXSwicm9sZSI6ImFkbWluIn0.DAjMaNFVF7chKUZQ65lMrYn6zWFGjX3gcoAiQuburqM'
HEADERS = {'Authorization': token}


async def test_fixture_test_erpsync_get(test_cli):
    """测试 ==> 接口"""
    params = {'rfid': ''}
    url = '/wabpcode'
    resp = await test_cli.get(url, params=params)
    assert resp.status == 200
    resp_json = await resp.json()
    print('url ==> {}, result ==> {}'.format(url, resp_json))
    assert resp_json.get('code') == 'SUCCESS'


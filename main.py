#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from sanic import Sanic
from sanic_cors import CORS
from app.views import web
from app.routes import setup_web_routes
from admin.views import admin
from admin.routes import setup_admin_routes
from utils.mysql import PyMySQL
from utils.cache import Cache
from utils.exceptions import SysError
from sanic_script import Manager


def setup_media(app):
    """设置MEDIA文件路由"""
    app.static('/media', app.config.MEDIA_DIR)


def setup_cors(app):
    """设置跨域"""
    headers = {
        'methods': 'GET, POST, DELETE, PUT, PATCH',
        'max_age': 1000,
    }
    CORS(app, automatic_options=True, **headers)


app = Sanic(__name__)
app.config.from_pyfile('config/settings.py')
setup_web_routes()
setup_admin_routes()
app.blueprint(web)
app.blueprint(admin)
setup_media(app)
setup_cors(app)


@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = await PyMySQL(loop, app.config.DATABASE)  # 获取mysql连接池
    app.cache = await Cache(loop, app.config.CACHE)  # 获取redis连接池


@app.listener('before_server_start')
async def setup_auth_key(app, loop):
    key = await app.db.get("select value from setting where codename = 'auth_key';")
    if not key:
        raise SysError('SysError', 'auth_key not found')
    app.config.auth_key = key['value']


@app.listener('after_server_stop')
async def close_db(app, loop):
    app.db.mysql_pool.close()  # 关闭mysql连接池
    await app.db.mysql_pool.wait_closed()
    app.cache.reids_pool.close()  # 关闭redis连接池
    await app.cache.reids_pool.wait_closed()


@app.middleware('response')
async def custom_banner(request, response):
    """设置响应自定义头部信息"""
    # host = request.headers.get('host')
    headers = {
        "Server": '梦工场',
        "x-xss-protection": "1; mode=block",
        # 'Access-Control-Allow-Origin': host,
        # 'Access-Control-Allow-Methods': 'GET, POST, DELETE, PUT, PATCH',
        # 'Access-Control-Max-Age': 1000,
        # 'Access-Control-Allow-Headers': '*'
    }
    for k, v in headers.items():
        response.headers[k] = v


manager = Manager(app)


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', default='9000')
@manager.option('-d', '--debug', dest='debug', default=False)
@manager.option('-a', '--auto', dest='auto_reload', default=False)
def start(host, port, debug, auto_reload):
    """启动sanic服务"""
    app.run(host=host, port=port, debug=debug, auto_reload=auto_reload)


if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser(description="sanic server start")
    # parser.add_argument('--host', type=str, default='0.0.0.0', help='this is a host')
    # parser.add_argument('--port', type=str, default='9000', help='this is a port')
    # args = parser.parse_args()
    # app.run(host=args.host, port=args.port, debug=False)
    manager.run()

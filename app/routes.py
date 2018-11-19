#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from app.views import *


def setup_web_routes():
    # web.add_route(Index.as_view(), '/', name='Index', strict_slashes=True)
    web.add_route(UserAuth.as_view(), '/auth', name='UserAuth')
    web.add_route(RefreshToken.as_view(), '/auth/refresh_token', name='RefreshToken')
    web.add_route(UserLogout.as_view(), '/auth/logout', name='UserLogout')
    web.add_route(UserMe.as_view(), '/users/me', name='UserMe')
    web.add_route(Pic.as_view(), '/pics', name='Pic')

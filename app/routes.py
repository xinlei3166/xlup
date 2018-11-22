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
    web.add_route(UserMePassword.as_view(), '/users/me/password', name='UserMePassword')
    web.add_route(UserMeHeadimg.as_view(), '/users/me/headimg', name='UserMeHeadimg')
    web.add_route(Pic.as_view(), '/pics', name='Pic')
    web.add_route(PicDetails.as_view(), '/pics/<pic_id>', name='PicDetails')
    web.add_route(Video.as_view(), '/videos', name='Video')
    web.add_route(VideoDetails.as_view(), '/videos/<video_id>', name='VideoDetails')

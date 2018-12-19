#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from admin import admin, views


def setup_admin_routes():
    admin.add_route(views.UserAdmin.as_view(), '/users', name='UserAdmin')
    admin.add_route(views.UserDetailsAdmin.as_view(), '/users/<uid>', name='UserDetailsAdmin')
    admin.add_route(views.PicAdmin.as_view(), '/pics', name='PicAdmin')
    admin.add_route(views.PicDetailsAdmin.as_view(), '/pics/<pic_id>', name='PicDetailsAdmin')
    admin.add_route(views.VideoAdmin.as_view(), '/videos', name='VideoAdmin')
    admin.add_route(views.VideoDetailsAdmin.as_view(), '/videos/<video_id>', name='VideoDetailsAdmin')

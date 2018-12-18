#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from admin import admin, views


def setup_admin_routes():
    admin.add_route(views.UserAdmin.as_view(), '/users', name='UserAdmin')
    admin.add_route(views.UserDetailsAdmin.as_view(), '/users/<uid>', name='UserDetailsAdmin')

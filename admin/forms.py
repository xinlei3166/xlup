#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from xlform import *


class UserAddForm(Form):
    username = RegexField(r'[0-9a-zA-Z]{4,20}', max_length=20)
    password = CharField(max_length=20, min_length=6)
    nickname = CharField(max_length=32, min_length=2)
    gender = RegexField(r'^(male|female)$', max_length=6)
    phone = RegexField(r'^1[356789]\d{9}', max_length=11, required=False)
    email = RegexField(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', max_length=64, required=False)

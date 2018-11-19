#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from xlform import *


class StyleUpdateForm(Form):
    name = CharField(max_length=30, min_length=2)
    theme = CharField(max_length=30, required=False)
    series = CharField(max_length=30, required=False)
    star = CharField(max_length=30, required=False)
    quarter = CharField(max_length=30, required=False)



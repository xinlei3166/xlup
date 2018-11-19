#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

from xlform import *
from sanic.request import File


class FileValidator:
    msg = 'invalid byte value'

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def __call__(self, value):
        if not isinstance(value, File):
            raise ValidationError(msg=self.msg)


validate_file = FileValidator()


class PicUploadForm(Form):
    """图片上传表单"""
    title = CharField(max_length=32, required=False)
    description = CharField(max_length=64, required=False)
    pic = Field(validators=[validate_file])

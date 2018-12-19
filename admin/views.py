#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import shortuuid
import itertools
import pathlib
from sanic.blueprints import Blueprint
from sanic.views import HTTPMethodView as View
from sanic import response
from utils.base import json_dumps
from utils.decorators import check_permission
from utils.paginator import Paginator
from utils.base import carry_key_hash_md5, hmac_sha256
from utils.access_key import generate_access_key_id, generate_access_key_secret
from . import forms

admin = Blueprint('admin', url_prefix='admin')


class UserAdmin(View):
    """用户列表"""

    @check_permission()
    async def get(self, request, **kwargs):
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get(
                "select count(id) as count from user where concat(`username`, ',', `nickname`, ',', `phone`, ',', `email`) like %s and delete_flag = 0;",
                ('%%%s%%' % q))
            count = count_res['count']
            res = await request.app.db.query(
                "select `id`, `username`, `nickname`, `gender`, `email`, `phone`, `create_time`, `update_time` from user where concat(`username`, ',', `nickname`, ',', `phone`, ',', `email`) like %s and delete_flag = 0 order by id desc limit %s, %s;",
                ('%%%s%%' % q, _start, per_page))
        else:
            count_res = await request.app.db.get("select count(id) as count from user where delete_flag = 0;")
            count = count_res['count']
            res = await request.app.db.query(
                "select `id`, `username`, `nickname`, `gender`, `email`, `phone`, `create_time`, `update_time` from user where delete_flag = 0 order by id desc limit %s, %s;",
                (_start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'Success', 'total': count, 'pages': pages, 'data': res}, dumps=json_dumps)

    @classmethod
    def generate_user_secret(cls, request):
        secret = carry_key_hash_md5(request.app.config.auth_key, shortuuid.ShortUUID().uuid())
        return secret

    @classmethod
    def generate_access_key(cls, key):
        access_key_id = generate_access_key_id()
        access_key_secret = generate_access_key_secret(key, access_key_id)
        return access_key_id, access_key_secret

    @classmethod
    async def add_user(cls, request, data):
        role = await request.app.db.get("select id from role where codename = %s", ("user",))
        if not role:
            return response.json({'code': 'SysError', 'msg': 'system error'}, dumps=json_dumps)
        secret = cls.generate_user_secret(request)
        data['password'] = hmac_sha256(secret, data['password'])
        _values = (
            data['username'], data['password'], data['nickname'], data['gender'], data['phone'], data['email'],
            role['id'])
        sql = "insert into user(username, password, nickname, gender, phone, email, role_id) values(%s, %s, %s, %s, %s, %s, %s)"
        user_id = await request.app.db.create(sql, _values)
        if not user_id:
            return response.json({'code': 'UserAddFail', 'msg': 'user add fail'}, dumps=json_dumps)
        user_secret = await request.app.db.create("insert into user_secret(user_id, secret) values(%s, %s)",
                                                  (user_id, secret))
        access_key = await request.app.db.create(
            "insert into access_key(user_id, access_key_id, access_key_secret) values(%s, %s, %s)",
            tuple(itertools.chain([user_id], cls.generate_access_key(request.app.config.auth_key))))
        if user_secret and access_key:
            return response.json({'code': 'Success'}, dumps=json_dumps)
        return response.json({'code': 'UserAddFail', 'msg': 'user add fail'}, dumps=json_dumps)

    @check_permission()
    async def post(self, request, **kwargs):
        data = {k: request.form.get(k) for k in request.form}
        form = forms.UserAddForm(data)
        if form.is_valid():
            form_data = form.cleaned_data
            return await self.add_user(request, form_data)
        else:
            return response.json({'code': 'InvalidParams', 'msg': form.errors}, dumps=json_dumps)


class UserDetailsAdmin(View):
    """单个用户"""

    @classmethod
    async def validate_nickname(cls, nickname, **kwargs):
        """验证昵称"""
        if not re.fullmatch(r'\w{2,32}', nickname):
            return response.json(
                {'code': 'InvalidNickname', 'msg': 'nickname ==> min_length: 2, max_length: 32'})

    @classmethod
    async def validate_gender(cls, gender, **kwargs):
        """验证性别"""
        if not re.fullmatch(r'^(male|female)$', gender):
            return response.json(
                {'code': 'InvalidGender', 'msg': 'gender ==> (male|female)'})

    @classmethod
    async def validate_phone(cls, phone, **kwargs):
        """验证手机号"""
        if not re.fullmatch(r'^1[356789]\d{9}', phone):
            return response.json({'code': 'InvalidPhone', 'msg': 'invalid phone'})
        else:
            user = kwargs.get('user')
            db = kwargs.get('db')
            if phone != user['phone']:
                res = await db.get("select user.id from user where user.phone = %s;", (phone,))
                if res:
                    return response.json({'code': 'PhoneExist', 'msg': 'phone exist'})

    @classmethod
    async def validate_email(cls, email, **kwargs):
        """验证手机号"""
        if not re.fullmatch(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', email):
            return response.json({'code': 'InvalidEmail', 'msg': 'invalid email'})
        else:
            user = kwargs.get('user')
            db = kwargs.get('db')
            if email != user['email']:
                res = await db.get("select user.id from user where user.email = %s;", (email,))
                if res:
                    return response.json({'code': 'EmailExist', 'msg': 'email exist'})

    @classmethod
    async def validate_password(cls, password, **kwargs):
        """验证密码"""
        if not re.fullmatch(r'\w{6,20}', password):
            return response.json(
                {'code': 'user.InvalidPassword', 'msg': 'password ==> min_length: 6, max_length: 20'})

    @classmethod
    def clean(cls, user, data):
        cleaned_data = dict(data)
        if cleaned_data.get('password'):
            cleaned_data['password'] = hmac_sha256(user['secret'], cleaned_data['password'])
        return cleaned_data

    @classmethod
    async def change_user_and_write_table(cls, db, user, keys=(), values=()):
        """修改用户信息并写入数据库"""
        field = ','.join(["%s=%%s" % key for key in keys])
        sql = "update user set {} where user.id = %s;".format(field)
        res = await db.update(sql, tuple(itertools.chain(values, [user['id']])))
        if res is None:
            return response.json({'code': 'UpdateUserinfoFail', 'msg': 'update userinfo fail'})
        return response.json({'code': 'Success'})

    @check_permission()
    async def patch(self, request, uid, **kwargs):
        """修改用户部分信息"""
        user_id = uid
        user = await request.app.db.get(
            "select user.id, user.username, user.nickname, user.gender, user.phone, user.email, user_secret.secret from user join user_secret on user.id = user_secret.user_id where user.delete_flag = 0 and user.id = %s;",
            (user_id,))
        if not user:
            return response.json({'code': 'UsernameNotExist', 'msg': 'username not exist'})
        allows = ('nickname', 'gender', 'phone', 'email', 'password')
        data = {k: request.form.get(k) for k in request.form.keys()}
        db = request.app.db
        for k, v in data.items():
            if k not in allows:
                return response.json({'code': 'InvalidParams', 'msg': 'contains invalid params'})
            if v:
                res = await getattr(self, 'validate_{}'.format(k))(v, user=user, db=db)
                if res:
                    return res
        cleaned_data = self.clean(user, data)
        return await self.change_user_and_write_table(db, user, tuple(cleaned_data.keys()),
                                                      tuple(cleaned_data.values()))

    @check_permission()
    async def delete(self, request, uid, **kwargs):
        """删除用户"""
        user_id = uid
        user = await request.app.db.get(
            "select user.id, user.username, user.nickname, user.gender, user.phone, user.email, user_secret.secret from user join user_secret on user.id = user_secret.user_id where user.delete_flag = 0 and user.id = %s;",
            (user_id,))
        if not user:
            return response.json({'code': 'UsernameNotExist', 'msg': 'username not exist'})
        allows = ('nickname', 'gender', 'phone', 'email', 'password')
        data = {k: request.form.get(k) for k in request.form.keys()}
        db = request.app.db
        for k, v in data.items():
            if k not in allows:
                return response.json({'code': 'InvalidParams', 'msg': 'contains invalid params'})
            if v:
                res = await getattr(self, 'validate_{}'.format(k))(v, user=user, db=db)
                if res:
                    return res
        cleaned_data = self.clean(user, data)
        return await self.change_user_and_write_table(db, user, tuple(cleaned_data.keys()),
                                                      tuple(cleaned_data.values()))


class PicAdmin(View):
    """图片"""

    @check_permission()
    async def get(self, request, **kwargs):
        """查看图片"""
        prefix = "{}/media/".format(request.app.config.UPLOAD_DOMAIN)
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get(
                "select count(id) as count from pic where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and pic.`delete_flag` = 0;",
                ('%%%s%%' % q,))
            count = count_res['count']
            res = await request.app.db.query(
                "select pic.`id`, pic.`title`, pic.`description`, concat(%s, pic.`path`) as pic, ifnull(user.`nickname`, '未知') as user, pic.`create_time`, pic.`update_time` from pic left join user on pic.user_id = user.id where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and pic.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, '%%%s%%' % q, _start, per_page))
        else:
            count_res = await request.app.db.get(
                "select count(id) as count from pic where pic.`delete_flag` = 0;")
            count = count_res['count']
            res = await request.app.db.query(
                "select pic.`id`, pic.`title`, pic.`description`, concat(%s, pic.`path`) as pic, ifnull(user.nickname, '未知') as user, pic.`create_time`, pic.`update_time` from pic left join user on pic.user_id = user.id where pic.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, _start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'Success', 'total': count, 'pages': pages, 'data': res}, dumps=json_dumps)


class PicDetailsAdmin(View):
    """单个图片"""

    @check_permission()
    async def delete(self, request, pic_id, **kwargs):
        """删除图片"""
        pic = await request.app.db.get(
            "select pic.id, pic.path from pic where delete_flag = 0 and pic.id = %s",
            (pic_id,))
        if not pic:
            return response.json({'code': 'PicNotExist', 'msg': 'pic not exist'})
        path = pathlib.Path(request.app.config.MEDIA_DIR)
        filepath = path.joinpath(pic['path'])
        if filepath.exists():
            filepath.unlink()
        res = await request.app.db.delete("delete from pic where pic.id = %s",
                                          (pic_id,))
        if res is not None:
            return response.json({'code': 'Success'})
        return response.json({'code': 'DeletePicFail', 'msg': 'delete pic fail'})


class VideoAdmin(View):
    """视频"""

    @check_permission()
    async def get(self, request, **kwargs):
        """查看视频"""
        prefix = "{}/media/".format(request.app.config.UPLOAD_DOMAIN)
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get(
                "select count(id) as count from video where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and video.`delete_flag` = 0;",
                ('%%%s%%' % q,))
            count = count_res['count']
            res = await request.app.db.query(
                "select video.`id`, video.`title`, video.`description`, concat(%s, video.`pic`) as pic, concat(%s, video.`path`) as video, ifnull(user.nickname, '未知') as user, video.`create_time`, video.`update_time` from video left join user on video.user_id = user.id where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and video.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, prefix, '%%%s%%' % q, _start, per_page))
        else:
            count_res = await request.app.db.get(
                "select count(id) as count from video where video.`delete_flag` = 0;")
            count = count_res['count']
            res = await request.app.db.query(
                "select video.`id`, video.`title`, video.`description`, concat(%s, video.`pic`) as pic, concat(%s, video.`path`) as video, ifnull(user.nickname, '未知') as user, video.`create_time`, video.`update_time` from video left join user on video.user_id = user.id where video.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, prefix, _start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'Success', 'total': count, 'pages': pages, 'data': res}, dumps=json_dumps)


class VideoDetailsAdmin(View):
    """单个视频"""

    @check_permission()
    async def delete(self, request, video_id, **kwargs):
        """删除视频"""
        video = await request.app.db.get(
            "select video.id, video.pic, video.path from video where delete_flag = 0 and video.id = %s",
            (video_id,))
        if not video:
            return response.json({'code': 'VideoNotExist', 'msg': 'video not exist'})
        path = pathlib.Path(request.app.config.MEDIA_DIR)
        picpath = path.joinpath(video['pic'])
        if picpath.exists():
            picpath.unlink()
        videopath = path.joinpath(video['path'])
        if videopath.exists():
            videopath.unlink()
        res = await request.app.db.delete("delete from video where video.id = %s",
                                          (video_id,))
        if res is not None:
            return response.json({'code': 'Success'})
        return response.json({'code': 'DeleteVideoFail', 'msg': 'delete video fail'})

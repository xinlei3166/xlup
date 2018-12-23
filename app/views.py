#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import time
import json
import pathlib
import datetime
import shortuuid
import collections
import itertools
from sanic.blueprints import Blueprint
from sanic.views import HTTPMethodView as View
from sanic import response
from .utils import CACHE_PREFIX
from jwt import InvalidTokenError, ExpiredSignature
from utils.base import json_dumps, hmac_sha256, hashid_encode, hashid_decode
from utils.token import token
from utils.exceptions import APIParameterError
from utils.decorators import check_token, check_permission, cache, check_access_sign
from utils.paginator import Paginator
from utils.access_key import generate_access_key_id, generate_access_key_secret, get_access_key, generate_policy, generate_policy_sign
from . import forms

web = Blueprint('xlup')


class UserAuth(View):
    """用户认证，获得授权"""

    @classmethod
    async def generate_token(cls, request, user, *, token_type):
        key = request.app.config.auth_key
        if token_type == 'refresh_token':  # 生成refresh_token
            _token = token.generate_refresh_token(key,
                                                  sub=hashid_encode(request.app.config.HASH_KEY, user['id']),
                                                  expires_in=token.refresh_expires_in,
                                                  # expires_in=10,
                                                  role=user['role_codename'])
        else:  # 生成access_token
            _token = token.generate_access_token(key,
                                                 sub=hashid_encode(request.app.config.HASH_KEY, user['id']),
                                                 expires_in=token.access_expires_in,
                                                 # expires_in=5,
                                                 role=user['role_codename'])
        return _token

    async def login(self, request):
        """账户登录"""
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            return response.json({'code': 'InvalidParams', 'msg': 'invalid params'})
        user = await request.app.db.get(
            "select user.id, user.username, user.password, user_secret.secret, role.codename as role_codename from user join user_secret join role on user.id = user_secret.user_id and user.role_id = role.id where user.username = %s;",
            (username,))
        if not user:
            return response.json({'code': 'UsernameNotExist', 'msg': 'username not exist'})
        if user['password'] == hmac_sha256(user['secret'], password):
            return response.json(
                {'code': 'Success',
                 'data': {'access_token': await self.generate_token(request, user, token_type='access_token'),
                          'refresh_token': await self.generate_token(request, user,
                                                                     token_type='refresh_token')}})
        else:
            return response.json({'code': 'IncorrectPassword', 'msg': 'incorrect password'})

    async def post(self, request):
        return await self.login(request)


class RefreshToken(View):
    """刷新token"""

    async def post(self, request):
        refresh_token = request.form.get('refresh_token')
        if not refresh_token:
            return response.json({'code': 'InvalidParams', 'msg': 'missing refresh_token'})
        revoke_refresh_token = await request.app.cache.get('refresh_token_{}'.format(refresh_token))
        if revoke_refresh_token:
            return response.json({'code': 'TokenRevoke', 'msg': 'token revoke'})
        key = request.app.config.auth_key
        try:
            payload = token.decode(key, refresh_token)
        except ExpiredSignature:
            return response.json({'code': 'RefreshTokenExpires', 'msg': 'refresh_token expires'})
        except InvalidTokenError:
            return response.json({'code': 'InvalidRefreshToken', 'msg': 'invalid refresh_token'})
        user_id = hashid_decode(request.app.config.HASH_KEY, payload.get('sub'))
        user = await request.app.db.get(
            "select user.id, user.username, role.codename as role_codename from user join role on user.role_id = role.id where user.id = %s;",
            (user_id,))
        if not user:
            return response.json({'code': 'InvalidTokenSub', 'msg': 'invalid access_token sub'})
        else:
            return response.json(
                {'code': 'Success',
                 'data': {'access_token': await UserAuth.generate_token(request, user,
                                                                        token_type='access_token')}})


class UserLogout(View):
    """用户注销"""

    async def post(self, request, **kwargs):
        access_token = request.form.get('access_token')
        refresh_token = request.form.get('refresh_token')
        if not all([access_token, refresh_token]):
            return response.json({'code': 'InvalidParams', 'msg': 'missing access_token or refresh_token'})
        key = request.app.config.auth_key
        try:
            access_payload = token.decode(key, access_token)
        except ExpiredSignature:
            return response.json({'code': 'AccessTokenExpires', 'msg': 'access_token expires'})
        except InvalidTokenError:
            return response.json({'code': 'InvalidAccessToken', 'msg': 'invalid access_token'})
        try:
            refresh_payload = token.decode(key, refresh_token)
        except ExpiredSignature:
            return response.json({'code': 'RefreshTokenExpires', 'msg': 'refresh_token expires'})
        except InvalidTokenError:
            return response.json({'code': 'InvalidRefreshToken', 'msg': 'invalid refresh_token'})
        now = int(time.time())
        await request.app.cache.set('access_token_{}'.format(access_token), json.dumps(False),
                                    expire=access_payload.get('exp') - now)
        await request.app.cache.set('refresh_token_{}'.format(refresh_token), json.dumps(False),
                                    expire=refresh_payload.get('exp') - now)
        return response.json({'code': 'Success'})


class UserMe(View):
    """用户自身信息"""

    # @cache(expire=60 * 60 * 24)
    async def get_userinfo(self, request, user_id, **kwargs):
        # cache_key = kwargs.get('cache_key')
        # expire = kwargs.get('expire')
        prefix = "{}/media/".format(request.app.config.UPLOAD_DOMAIN)
        default_head_img = "default.png"
        userinfo = await request.app.db.get(
            "select user.nickname, concat(%s, ifnull(user.head_img, %s)) as head_img, user.gender, user.email, user.phone, role.name as role_name, role.codename as role_codename from user join role on user.role_id = role.id where user.id = %s;",
            (prefix, default_head_img, user_id))
        # await request.app.cache.set(cache_key, json.dumps(userinfo), expire=expire)
        return userinfo

    @check_token
    async def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        cache_key = CACHE_PREFIX % 'userme:{}'.format(user_id)
        userinfo = await self.get_userinfo(request, user_id, cache_key=cache_key)
        return response.json({'code': 'Success', 'data': userinfo})

    @classmethod
    async def validate_nickname(cls, nickname, **kwargs):
        """验证昵称"""
        if not re.fullmatch(r'[\s\w-]{2,20}', nickname):
            return response.json(
                {'code': 'InvalidNickname', 'msg': 'nickname ==> min_length: 2, max_length: 20'})

    @classmethod
    async def validate_gender(cls, gender, **kwargs):
        """验证性别"""
        if gender not in ['male', 'female']:
            return response.json({'code': 'InvalidGender', 'msg': 'gender ==> male or female'})

    @classmethod
    async def validate_phone(cls, phone, **kwargs):
        """验证手机号"""
        if not re.match('^1[3456789]\d{9}$', phone):
            return response.json(
                {'code': 'InvalidPhone', 'msg': 'phone ==> length: 11, format: 1[3456789]\d{9}'})
        user = kwargs.get('user')
        db = kwargs.get('db')
        if phone != user['phone']:
            res = await db.get("select user.id from user where user.phone = %s;", (phone,))
            if res:
                return response.json({'code': 'PhoneExist', 'msg': 'phone exist'})

    @classmethod
    async def validate_email(cls, email, **kwargs):
        """验证邮箱"""
        if not re.match(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$', email):
            return response.json({'code': 'InvalidEmail', 'msg': 'email ==> xxx@qq.com}'})
        user = kwargs.get('user')
        db = kwargs.get('db')
        if email != user['email']:
            res = await db.get("select user.id from user where user.email = %s;", (email,))
            if res:
                return response.json({'code': 'EmailExist', 'msg': 'email exist'})

    @classmethod
    async def write_table(cls, db, user, keys=(), values=()):
        """写入数据库"""
        field = ','.join(["%s=%%s" % key for key in keys])
        sql = "update user set {} where user.id = %s;".format(field)
        res = await db.update(sql, tuple(itertools.chain(values, [user['id']])))
        if res is None:
            return response.json({'code': 'UpdateUserinfoFail', 'msg': 'update userinfo fail'})
        return response.json({'code': 'Success'})

    @check_token
    async def patch(self, request, **kwargs):
        """修改用户部分信息"""
        user_id = kwargs.get('user_id')
        user = await request.app.db.get(
            "select user.id, user.username, user.nickname, user.gender, user.phone, user.email from user where user.id = %s;",
            (user_id,))
        if not user:
            return response.json({'code': 'UsernameNotExist', 'msg': 'username not exist'})
        allows = ('nickname', 'gender', 'phone', 'email')
        data = {k: request.form.get(k) for k in request.form.keys()}
        db = request.app.db
        for k, v in data.items():
            if k not in allows:
                return response.json({'code': 'InvalidParams', 'msg': 'contains invalid params'})
            if v:
                res = await getattr(self, 'validate_{}'.format(k))(v, user=user, db=db)
                if res:
                    return res
        return await self.write_table(db, user, tuple(data.keys()), tuple(data.values()))


class UserMePassword(View):
    """用户密码"""

    @classmethod
    async def change_password(cls, request, user):
        """修改密码"""
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        if not all([old_password, new_password]):
            return response.json({'code': 'InvalidParams', 'msg': 'missing params'})
        if user['password'] != hmac_sha256(user['secret'], old_password):
            return response.json({'code': 'IncorrectOldPassword', 'msg': 'incorrect old password'})
        if not re.fullmatch(r'\w{6,20}', new_password):
            return response.json(
                {'code': 'user.InvalidNewPassword', 'msg': 'new password ==> min_length: 6, max_length: 20'})
        password = hmac_sha256(user['secret'], new_password)
        res = await request.app.db.update("update user set user.password = %s where user.id = %s;",
                                          (password, user['id']))
        if res is None:
            return response.json({'code': 'UpdatePasswordFail', 'msg': 'update password fail'})
        return response.json({'code': 'Success'})

    @check_token
    async def put(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        user = await request.app.db.get(
            "select user.id, user.username, user.password, user_secret.secret from user join user_secret on user.id = user_secret.user_id where user.id = %s;",
            (user_id,))
        if not user:
            return response.json({'code': 'UsernameNotExist', 'msg': 'username not exist'})
        return await self.change_password(request, user)


class UserMeHeadimg(View):
    """用户头像"""

    # @classmethod
    # def change_head_image(cls, head_img):
    #     """修改头像"""
    #     reg = re.compile(r'^{}(.*?)$'.format(request.app.config.UPLOAD_DOMAIN))
    #     try:
    #         _head_img = reg.findall(head_img).pop()
    #     except IndexError:
    #         return response.json({'code': 'InvalidHeadimg', 'msg': 'invalid head_img'})
    #     else:
    #         return _head_img

    @classmethod
    async def change_head_image(cls, request, user_id):
        """修改头像"""
        head_img = request.files.get('head_img', None)
        if head_img is None:
            return response.json({'code': 'InvalidParams', 'msg': 'missing head_img'})
        # try:
        #     content = base64.b64decode(head_img.split(',')[1])  # 图片内容
        #     suffix = head_img.split(';')[0].split('/')[1] if len(head_img.split(';')) == 2 else 'png'  # 图片后缀名
        # except (IndexError, binascii.Error):
        #     return response.json({'code': 'InvalidHeadimg', 'msg': 'invalid head_img'})
        content = head_img.body
        suffix = head_img.type.split('/')[1]
        path = pathlib.Path(request.app.config.MEDIA_DIR)
        rel_path = datetime.datetime.now().strftime('%Y/%m/%d')
        filename = "{}.{}".format(shortuuid.ShortUUID().random(length=12), suffix)
        filepath = path.joinpath('pic', rel_path, filename)
        media_path = pathlib.Path('pic', rel_path, filename)
        media_path = str(media_path.relative_to('.'))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open('wb') as f:
            f.write(content)
        if not filepath.exists():
            return response.json({'code': 'UpdateHeadimgFail', 'msg': 'update headimg fail'})
        user = await request.app.db.get("select user.head_img from user where user.id = %s", (user_id,))
        old_head_img = user['head_img']
        if old_head_img:
            old_filepath = path.joinpath(old_head_img)
            old_filepath.unlink()
        res = await request.app.db.update(
            "update user set head_img = %s where id = %s;", (media_path, user_id))
        if res is None:
            return response.json({'code': 'UpdateHeadimgFail', 'msg': 'update headimg fail'})
        return response.json({'code': 'Success'})

    @check_token
    async def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        return await self.change_head_image(request, user_id)


class UserMeAccessKey(View):
    """用户上传秘钥"""

    @check_token
    async def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        access_key = await request.app.db.get(
            "select access_key_id, access_key_secret, create_time from access_key where user_id = %s;",
            (user_id,))
        if access_key:
            return response.json({'code': 'Success', 'data': access_key}, dumps=json_dumps)
        return response.json({'code': 'AccessKeyNotExist', 'msg': 'access key not exist'}, dumps=json_dumps)

    @check_token
    async def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        access_key_id = generate_access_key_id()
        access_key_secret = generate_access_key_secret(request.app.config.auth_key, access_key_id)
        access_key = await request.app.db.get("select id from access_key where user_id = %s;", (user_id,))
        if access_key:
            return response.json({'code': 'AccessKeyExist', 'msg': 'access key exist'}, dumps=json_dumps)
        res = await request.app.db.create(
            "insert into access_key(user_id, access_key_id, access_key_secret) values(%s, %s, %s)",
            (user_id, access_key_id, access_key_secret))
        if res:
            return response.json(
                {'code': 'Success',
                 'data': {'access_key_id': access_key_id, 'access_key_secret': access_key_secret}},
                dumps=json_dumps)
        return response.json({'code': 'NewAccessKeyFail', 'msg': 'new access key fail'}, dumps=json_dumps)


class UploadPolicy(View):
    """获取upload policy, form表单上传使用"""

    @check_token
    async def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        access_key = await get_access_key(request.app.db, user_id)
        if not access_key:
            return response.json({'code': 'AccessKeyNotExist', 'msg': 'access key not exist'}, dumps=json_dumps)
        access_key_id = access_key['access_key_id']
        policy = generate_policy()
        sign = generate_policy_sign(access_key['access_key_secret'], policy)
        data = {'access_key_id': access_key_id, 'policy': policy, 'sign': sign}
        return response.json({'code': 'Success', 'data': data})


class Pic(View):
    """图片"""

    @check_token
    async def get(self, request, **kwargs):
        """查看图片"""
        user_id = kwargs.get('user_id')
        prefix = "{}/media/".format(request.app.config.UPLOAD_DOMAIN)
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get(
                "select count(id) as count from pic where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and pic.`user_id` = %s and pic.`delete_flag` = 0;",
                ('%%%s%%' % q, user_id))
            count = count_res['count']
            res = await request.app.db.query(
                "select pic.`id`, pic.`title`, pic.`description`, concat(%s, pic.`path`) as pic, pic.`create_time`, pic.`update_time` from pic where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and pic.`user_id` = %s and pic.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, '%%%s%%' % q, user_id, _start, per_page))
        else:
            count_res = await request.app.db.get(
                "select count(id) as count from pic where pic.`user_id` = %s and pic.`delete_flag` = 0;",
                (user_id,))
            count = count_res['count']
            res = await request.app.db.query(
                "select pic.`id`, pic.`title`, pic.`description`, concat(%s, pic.`path`) as pic, pic.`create_time`, pic.`update_time` from pic where pic.`user_id` = %s and pic.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, user_id, _start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'Success', 'total': count, 'pages': pages, 'data': res}, dumps=json_dumps)

    @classmethod
    def write_pic(cls, path, pic):
        rel_path = datetime.datetime.now().strftime('%Y/%m/%d')
        suffix = pic.type.split('/')[-1]
        filename = "{}.{}".format(shortuuid.ShortUUID().random(length=12), suffix)
        filepath = path.joinpath('pic', rel_path, filename)
        media_path = pathlib.Path('pic', rel_path, filename)
        media_path = str(media_path.relative_to('.'))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open('wb') as f:
            f.write(pic.body)
        if filepath.exists():
            return media_path

    @classmethod
    async def upload_pic(cls, request, user_id, data):
        form = forms.PicUploadForm(data)
        if form.is_valid():
            form_data = form.cleaned_data
            pic = form_data['pic']
            file_type = pic.type.split('/')[0]
            if file_type != 'image':
                return response.json({'code': 'PicFormatError', 'msg': 'pic format error'})
            path = pathlib.Path(request.app.config.MEDIA_DIR)
            media_path = cls.write_pic(path, pic)
            if not media_path:
                return response.json({'code': 'UploadFail', 'msg': 'uplopad pic fail'})
            res = await request.app.db.create(
                "insert into pic(pic.`user_id`, pic.`title`, pic.`description`, pic.`path`) values(%s, %s, %s, %s);",
                (user_id, form_data['title'], form_data['description'], media_path))
            if not res:
                return response.json({'code': 'UploadFail', 'msg': 'uplopad pic fail'})
            _data = {'title': form_data['title'], 'description': form_data['description'],
                     'pic': "{}/media/{}".format(request.app.config.UPLOAD_DOMAIN, media_path)}
            return response.json({'code': 'Success', 'data': _data})
        else:
            return response.json({'code': 'InvalidParams', 'msg': form.errors})

    @check_token
    async def post(self, request, **kwargs):
        """上传图片"""
        user_id = kwargs.get('user_id')
        data = {k: request.form.get(k) for k in request.form.keys()}
        _file = {k: request.files.get(k) for k in request.files.keys()}
        data.update(_file)
        return await self.upload_pic(request, user_id, data)


class PicDetails(View):
    """单个图片"""

    @check_token
    async def delete(self, request, pic_id, **kwargs):
        """删除图片"""
        user_id = kwargs.get('user_id')
        pic = await request.app.db.get(
            "select pic.id, pic.path from pic where pic.user_id = %s and pic.id = %s",
            (user_id, pic_id))
        if not pic:
            return response.json({'code': 'PicNotExist', 'msg': 'pic not exist'})
        path = pathlib.Path(request.app.config.MEDIA_DIR)
        filepath = path.joinpath(pic['path'])
        if filepath.exists():
            filepath.unlink()
        res = await request.app.db.delete("delete from pic where pic.user_id = %s and pic.id = %s",
                                          (user_id, pic_id))
        if res is not None:
            return response.json({'code': 'Success'})
        return response.json({'code': 'DeletePicFail', 'msg': 'delete pic fail'})


class PicUnAuth(View):
    """图片"""

    @check_access_sign
    async def post(self, request, **kwargs):
        """上传图片"""
        user_id = kwargs.get('user_id')
        data = {k: request.form.get(k) for k in request.form.keys()}
        _file = {k: request.files.get(k) for k in request.files.keys()}
        data.update(_file)
        return await Pic.upload_pic(request, user_id, data)


class Video(View):
    """视频"""

    @check_token
    async def get(self, request, **kwargs):
        """查看视频"""
        user_id = kwargs.get('user_id')
        prefix = "{}/media/".format(request.app.config.UPLOAD_DOMAIN)
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get(
                "select count(id) as count from video where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and video.`user_id` = %s and video.`delete_flag` = 0;",
                ('%%%s%%' % q, user_id))
            count = count_res['count']
            res = await request.app.db.query(
                "select video.`id`, video.`title`, video.`description`, concat(%s, video.`pic`) as pic, concat(%s, video.`path`) as video, video.`create_time`, video.`update_time` from video where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and video.`user_id` = %s and video.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, prefix, '%%%s%%' % q, user_id, _start, per_page))
        else:
            count_res = await request.app.db.get(
                "select count(id) as count from video where video.`user_id` = %s and video.`delete_flag` = 0;",
                (user_id,))
            count = count_res['count']
            res = await request.app.db.query(
                "select video.`id`, video.`title`, video.`description`, concat(%s, video.`pic`) as pic, concat(%s, video.`path`) as video, video.`create_time`, video.`update_time` from video where video.`user_id` = %s and video.`delete_flag` = 0 order by id desc limit %s, %s;",
                (prefix, prefix, user_id, _start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'Success', 'total': count, 'pages': pages, 'data': res}, dumps=json_dumps)

    @classmethod
    def write_video(cls, path, video):
        rel_path = datetime.datetime.now().strftime('%Y/%m/%d')
        suffix = video.type.split('/')[-1]
        filename = "{}.{}".format(shortuuid.ShortUUID().random(length=12), suffix)
        filepath = path.joinpath('video', rel_path, filename)
        media_path = pathlib.Path('video', rel_path, filename)
        media_path = str(media_path.relative_to('.'))
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with filepath.open('wb') as f:
            f.write(video.body)
        if filepath.exists():
            return media_path

    @classmethod
    async def upload_video(cls, request, user_id, data):
        form = forms.VideoUploadForm(data)
        if form.is_valid():
            form_data = form.cleaned_data
            pic = form_data['pic']
            pic_type = pic.type.split('/')[0]
            if pic_type != 'image':
                return response.json({'code': 'PicFormatError', 'msg': 'pic format error'})
            video = form_data['video']
            video_type = video.type.split('/')[0]
            if video_type != 'video':
                return response.json({'code': 'VideoFormatError', 'msg': 'video format error'})
            path = pathlib.Path(request.app.config.MEDIA_DIR)
            pic_media_path = Pic.write_pic(path, pic)
            video_media_path = cls.write_video(path, video)
            if not pic_media_path or not video_media_path:
                return response.json({'code': 'UploadFail', 'msg': 'uplopad video fail'})
            res = await request.app.db.create(
                "insert into video(video.`user_id`, video.`title`, video.`description`, video.`pic`, video.`path`) values(%s, %s, %s, %s, %s);",
                (user_id, form_data['title'], form_data['description'], pic_media_path, video_media_path))
            if not res:
                return response.json({'code': 'UploadFail', 'msg': 'uplopad pic fail'})
            _data = {'title': form_data['title'], 'description': form_data['description'],
                     'pic': "{}/media/{}".format(request.app.config.UPLOAD_DOMAIN, pic_media_path),
                     'video': "{}/media/{}".format(request.app.config.UPLOAD_DOMAIN, video_media_path)}
            return response.json({'code': 'Success', 'data': _data})
        else:
            return response.json({'code': 'InvalidParams', 'msg': form.errors})

    @check_token
    async def post(self, request, **kwargs):
        """上传视频"""
        user_id = kwargs.get('user_id')
        data = {k: request.form.get(k) for k in request.form.keys()}
        _file = {k: request.files.get(k) for k in request.files.keys()}
        data.update(_file)
        return await self.upload_video(request, user_id, data)


class VideoDetails(View):
    """单个视频"""

    @check_token
    async def delete(self, request, video_id, **kwargs):
        """删除视频"""
        user_id = kwargs.get('user_id')
        video = await request.app.db.get(
            "select video.id, video.pic, video.path from video where video.user_id = %s and video.id = %s",
            (user_id, video_id))
        if not video:
            return response.json({'code': 'VideoNotExist', 'msg': 'video not exist'})
        path = pathlib.Path(request.app.config.MEDIA_DIR)
        picpath = path.joinpath(video['pic'])
        if picpath.exists():
            picpath.unlink()
        videopath = path.joinpath(video['path'])
        if videopath.exists():
            videopath.unlink()
        res = await request.app.db.delete("delete from video where video.user_id = %s and video.id = %s",
                                          (user_id, video_id))
        if res is not None:
            return response.json({'code': 'Success'})
        return response.json({'code': 'DeleteVideoFail', 'msg': 'delete video fail'})


class VideoUnAuth(View):
    """视频"""

    @check_access_sign
    async def post(self, request, **kwargs):
        """上传视频"""
        user_id = kwargs.get('user_id')
        data = {k: request.form.get(k) for k in request.form.keys()}
        _file = {k: request.files.get(k) for k in request.files.keys()}
        data.update(_file)
        return await Video.upload_video(request, user_id, data)

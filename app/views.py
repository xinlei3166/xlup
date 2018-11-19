#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import time
import json
import pathlib
import datetime
import base64
import binascii
import shortuuid
from sanic.blueprints import Blueprint
from sanic.views import HTTPMethodView as View
from sanic import response
from .utils import CACHE_PREFIX
from jwt import InvalidTokenError, ExpiredSignature
from utils.base import json_dumps, hmac_sha256, hashid_encode, hashid_decode
from utils.token import token
from utils.exceptions import APIParameterError
from utils.decorators import check_token, check_permission, cache
from utils.paginator import Paginator
from .forms import PicUploadForm

web = Blueprint('xlup', url_prefix='api')


class UserAuth(View):
    """用户认证，获得授权"""

    @classmethod
    async def generate_token(cls, request, user, *, token_type):
        key = request.app.config.auth_key
        if token_type == 'refresh_token':  # 生成refresh_token
            _token = token.generate_refresh_token(key, sub=hashid_encode(request.app.config.HASH_KEY, user['id']),
                                                  expires_in=token.refresh_expires_in,
                                                  role=user['role_codename'])
        else:  # 生成access_token
            _token = token.generate_access_token(key, sub=hashid_encode(request.app.config.HASH_KEY, user['id']),
                                                 expires_in=token.access_expires_in,
                                                 role=user['role_codename'])
        return _token

    async def login(self, request):
        """账户登录"""
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
                          'refresh_token': await self.generate_token(request, user, token_type='refresh_token')}})
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
                {'code': 'SUCCESS',
                 'data': {'access_token': await UserAuth.generate_token(request, user, token_type='access_token')}})


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
        return response.json({'code': 'SUCCESS'})


class UserMe(View):
    """用户自身信息"""

    @cache(expire=60 * 60 * 24)
    async def get_userinfo(self, request, user_id, **kwargs):
        cache_key = kwargs.get('cache_key')
        expire = kwargs.get('expire')
        default_head_img = "{}/media/default.png".format(request.app.config.UPLOAD_DOMAIN)
        userinfo = await request.app.db.get(
            "select user.id, user.username, user.nickname, ifnull(user.head_img, %s) as head_img, user.gender, user.email, user.phone, role.name as role_name from user join role on user.role_id = role.id where user.id = %s;",
            (default_head_img, user_id))
        await request.app.cache.set(cache_key, json.dumps(userinfo), expire=expire)
        return userinfo

    @check_token
    async def get(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        cache_key = CACHE_PREFIX % 'userme:{}'.format(user_id)
        userinfo = await self.get_userinfo(request, user_id, cache_key=cache_key)
        return response.json({'code': 'Success', 'data': userinfo})

    @classmethod
    def change_head_image(cls, request, head_img):
        """修改头像"""
        reg = re.compile(r'^{}(.*?)$'.format(request.app.config.UPLOAD_DOMAIN))
        try:
            _head_img = reg.findall(head_img).pop()
        except IndexError:
            pass    # todo here

    # @classmethod
    # def change_head_image(cls, head_img):
    #     """修改头像"""
    #     try:
    #         _content = base64.b64decode(head_img.split(',')[1])  # 图片内容
    #         _suffix = head_img.split(';')[0].split('/')[1] if len(head_img.split(';')) == 2 else 'png'  # 图片后缀名
    #     except (IndexError, binascii.Error):
    #         return response.json({'code': 'InvalidHeadimg', 'msg': 'invalid head_img'})
    #     _head_image = ContentFile(_content, shortuuid.ShortUUID().random(length=10) + '.{}'.format(_suffix))
    #     try:
    #         headimage = HeadImage.objects.get(shopmalluser=user)
    #     except HeadImage.DoesNotExist:
    #         headimage = HeadImage.objects.create(shopmalluser=user)
    #     headimage.head_image = _head_image
    #     headimage.save()

    # @classmethod
    # def change_nickname(cls, nickname, user):
    #     """修改昵称"""
    #     if not re.fullmatch(r'[\s\w-]{2,20}', nickname):
    #         return JsonResponse({'code': 'user.INVALID_NICKNAME', 'msg': 'nickname ==> min_length: 2, max_length: 20'})
    #     user.nickname = nickname
    #     user.save()
    #
    # @classmethod
    # def change_sex(cls, sex, user):
    #     """修改性别"""
    #     if sex not in ['男', '女']:
    #         return JsonResponse({'code': 'user.INVALID_SEX', 'msg': 'sex ==> 男 or 女'})
    #     user.sex = sex
    #     user.save()
    #
    # @classmethod
    # def change_phone_num(cls, phone_num, user):
    #     """修改手机号"""
    #     if not re.match('^1[3456789]\d{9}$', phone_num):
    #         return JsonResponse(
    #             {'code': 'user.INVALID_PHONE_NUM', 'msg': 'phone_num ==> length: 11, format: 1[3456789]\d{9}'})
    #     if phone_num != user.phone_num and User.objects.filter(phone_num=phone_num):
    #         return JsonResponse({'code': 'user.PHONENUM_EXIST', 'msg': 'phone number exist'})
    #     user.phone_num = phone_num
    #     user.save()
    #
    # @classmethod
    # def change_password(cls, password, user):
    #     """修改密码"""
    #     try:
    #         passwords = password.split(',')
    #         old_password = passwords[0]
    #         first_password = passwords[1]
    #         second_password = passwords[2]
    #     except IndexError:
    #         return response.json({'code': 'user.PASSWORD_FORMAT_ERROR', 'msg': 'password example: 123456,45678,45678'})
    #     usersecret = UserSecret.objects.get(uid=user.uid)
    #     if hmac_sha256(usersecret.secret, old_password) != user.password:
    #         return response.json({'code': 'user.OLDPASSWORD_INCORRECT', 'msg': 'old password incorrect'})
    #     if first_password != second_password:
    #         return response.json({'code': 'user.TWOPASSWORDS_NOT_MATCH', 'msg': 'the two passwords not match'})
    #     if not re.fullmatch(r'\w{6,20}', first_password):
    #         return response.json(
    #             {'code': 'user.INVALID_NEWPASSWORD', 'msg': 'new password ==> min_length: 6, max_length: 20'})
    #     user.password = hmac_sha256(usersecret.secret, first_password)
    #     user.save()
    #
    # @method_decorator(check_token)
    # def patch(self, request, **kwargs):
    #     """修改用户局部信息"""
    #     uid = kwargs.get('uid')
    #     try:
    #         user = User.objects.get(uid=uid, delete_flag=False)
    #     except User.DoesNotExist:
    #         return JsonResponse({'code': 'user.USER_NOT_EXIST', 'msg': 'user not exist'})
    #
    #     allows = ('head_image', 'nickname', 'sex', 'phone_num', 'password')
    #     data = {k: v for k, v in QueryDict(request.body, encoding='utf-8').items()}
    #     for k, v in data.items():
    #         if k not in allows:
    #             return response.json({'code': 'user.INVALID_PARAMS', 'msg': 'contains invalid params'})
    #         if v is not None:
    #             res = getattr(self, 'change_{}'.format(k))(v, user)
    #             if res:
    #                 return res
    #
    #     return response.json({'code': 'SUCCESS'})


class Pic(View):
    """图片"""

    @check_token
    async def get(self, request, **kwargs):
        """查看图片"""
        user_id = kwargs.get('user_id')
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get(
                "select count(id) as count from pic where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and pic.`user_id` = %s and pic.`delete_flag` = 0;", ('%%%s%%' % q, user_id))
            count = count_res['count']
            res = await request.app.db.query(
                "select pic.`id`, pic.`title`, pic.`description`, concat(%s, pic.`path`) as link, pic.`create_time`, pic.`update_time` from pic where concat(ifnull(`title`, ''), ',', ifnull(`description`, '')) like %s and pic.`user_id` = %s and pic.`delete_flag` = 0 order by id desc limit %s, %s;",
                (request.app.config.UPLOAD_DOMAIN, '%%%s%%' % q, user_id, _start, per_page))
        else:
            count_res = await request.app.db.get("select count(id) as count from pic where pic.`user_id` = %s and pic.`delete_flag` = 0;", (user_id,))
            count = count_res['count']
            res = await request.app.db.query(
                "select pic.`id`, pic.`title`, pic.`description`, concat(%s, pic.`path`) as link, pic.`create_time`, pic.`update_time` from pic where pic.`user_id` = %s and pic.`delete_flag` = 0 order by id desc limit %s, %s;",
                (request.app.config.UPLOAD_DOMAIN, user_id, _start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'SUCCESS', 'pages': pages, 'data': res}, dumps=json_dumps)

    @classmethod
    async def upload_pic(cls, request, user_id, data):
        form = PicUploadForm(data)
        if form.is_valid():
            form_data = form.cleaned_data
            pic = form_data['pic']
            path = pathlib.Path(request.app.config.MEDIA_DIR)
            media_path = pathlib.Path('/media')
            rel_path = datetime.datetime.now().strftime('%Y/%m/%d')
            suffix = pic.type.split('/')[-1]
            filename = "{}.{}".format(shortuuid.ShortUUID().random(length=12), suffix)
            filepath = path.joinpath('pic', rel_path, filename)
            media_path = media_path.joinpath('pic', rel_path, filename)
            media_path = str(media_path.resolve())
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with filepath.open('wb') as f:
                f.write(pic.body)
            if not filepath.exists():
                return response.json({'code': 'UploadFail', 'msg': 'uplopad pic fail'})
            res = await request.app.db.create(
                "insert into pic(pic.`user_id`, pic.`title`, pic.`description`, pic.`path`) values(%s, %s, %s, %s);",
                (user_id, form_data['title'], form_data['description'], media_path))
            if not res:
                return response.json({'code': 'UploadFail', 'msg': 'uplopad pic fail'})
            _data = {'title': form_data['title'], 'description': form_data['description'],
                     'link': "{}{}".format(request.app.config.UPLOAD_DOMAIN, media_path)}
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

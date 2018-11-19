#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import itertools
from sanic.blueprints import Blueprint
from sanic.views import HTTPMethodView as View
from sanic import response
from utils.base import json_dumps
from utils.exceptions import APIParameterError
from utils.decorators import check_token, check_permission
from utils.paginator import Paginator
from .forms import *

admin = Blueprint('admin', url_prefix='admin')


class StyleAdmin(View):
    """款式列表"""

    @check_permission('view_product')
    async def get(self, request, **kwargs):
        q = request.raw_args.get('q')
        page = int(request.raw_args.get('page', 1))
        per_page = int(request.raw_args.get('per_page', 10))
        _start = (page - 1) * per_page
        if q:
            count_res = await request.app.db.get("select count(id) as count from style where concat(`name`, ',', `serial`, ',', `theme`, ',', `series`, ',', `star`, ',',  `quarter`) like %s and delete_flag = 0;", ('%%%s%%' % q))
            count = count_res['count']
            res = await request.app.db.query("select `id`, `name`, `serial`, `tag_price`, `cert_code`, `theme`, `series`, `star`, `quarter`, `create_time`, `update_time` from style where concat(`name`, ',', `serial`, ',', `theme`, ',', `series`, ',', `star`, ',',  `quarter`) like %s and delete_flag = 0 order by id desc limit %s, %s;", ('%%%s%%' % q, _start, per_page))
        else:
            count_res = await request.app.db.get("select count(id) as count from style where delete_flag = 0;")
            count = count_res['count']
            res = await request.app.db.query("select `id`, `name`, `serial`, `tag_price`, `cert_code`, `theme`, `series`, `star`, `quarter`, `create_time`, `update_time` from style where delete_flag = 0 order by id desc limit %s, %s;", (_start, per_page))
        paginate = Paginator(count, per_page)
        pages = paginate()
        return response.json({'code': 'SUCCESS', 'pages': pages, 'data': res}, dumps=json_dumps)

    # @check_permission('add_product')
    # async def post(self, request, **kwargs):
    #     data = {k: request.form.get(k) for k in request.form}


class StyleDetailsAdmin(View):
    """单个款式"""

    @check_permission('change_product')
    async def put(self, request, sid, **kwargs):
        style = await request.app.db.get("select id from style where style.`delete_flag` = 0 and style.`id` = %s;", (sid,))
        if not style:
            return response.json({'code': 'commodity.STYLE_NOT_EXIST', 'msg': 'style not exist'})
        data = {k: request.form.get(k) for k in request.form}
        form = StyleUpdateForm(data)
        if form.is_valid():
            form_data = form.cleaned_data
            _style_params = tuple(itertools.chain(form_data.values(), [sid]))
            res = await request.app.db.update("update style set style.`name` = %s, style.`theme` = %s, style.`series` = %s, style.`star` = %s, style.`quarter` = %s where style.id = %s", _style_params)
            if res is not None:
                return response.json({'code': 'SUCCESS'})
            else:
                return response.json({'code': 'commodity.STYLE_UPDATE_FAIL', 'msg': 'style update fail'})
        else:
            return response.json({'code': 'commodity.INVALID_PARAMS', 'msg': form.errors})




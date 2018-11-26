from peewee import *
from config.settings import DATABASE

kwargs = {'charset': DATABASE['charset'], 'use_unicode': True, 'user': DATABASE['user'], 'password': DATABASE['password']}
db = MySQLDatabase(DATABASE['db'], **kwargs)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    delete_flag = BooleanField(verbose_name='删除标志', constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(verbose_name='创建时间', constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_time = DateTimeField(verbose_name='修改时间', constraints=[SQL("DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP")])

    class Meta:
        database = db


"""
tables = BaseModel.__subclasses__()

try:
    db.connect()
    db.create_tables(tables)
except BaseException:
    db.rollback()
else:
    db.close()
"""


class Setting(BaseModel):
    codename = CharField(max_length=64)
    name = CharField(verbose_name='项目名', max_length=64)
    value = CharField(verbose_name='项目值', max_length=64)

    class Meta:
        table_name = 'setting'


class AccessKey(BaseModel):
    user_id = IntegerField(verbose_name='用户', index=True)
    access_key_id = CharField(max_length=64)
    access_key_secret = CharField(max_length=64)

    class Meta:
        table_name = 'access_key'


class Role(BaseModel):
    codename = CharField(max_length=32, unique=True)
    name = CharField(verbose_name='角色名称', max_length=32, unique=True)
    description = CharField(verbose_name='描述', max_length=64, null=True)

    class Meta:
        table_name = 'role'


class User(BaseModel):
    username = CharField(verbose_name='用户名', max_length=64)
    password = CharField(verbose_name='密码', max_length=128)
    nickname = CharField(verbose_name='昵称', max_length=32)
    head_img = CharField(verbose_name='头像', max_length=64, constraints=[SQL("DEFAULT '/media/default.png'")])
    gender = CharField(verbose_name='性别', max_length=12, constraints=[SQL("DEFAULT 'female'")])
    email = CharField(verbose_name='邮箱', max_length=64, null=True, unique=True)
    phone = CharField(verbose_name='手机号', max_length=11, null=True, unique=True)
    role_id = IntegerField(verbose_name='角色')

    class Meta:
        table_name = 'user'


class UserSecret(BaseModel):
    user_id = IntegerField(verbose_name='用户', index=True)
    secret = CharField(verbose_name='秘钥', max_length=64)

    class Meta:
        table_name = 'user_secret'


class Pic(BaseModel):
    user_id = IntegerField(verbose_name='用户', index=True)
    title = CharField(verbose_name='标题', max_length=32, null=True)
    path = CharField(verbose_name='图片路径', max_length=128)
    description = CharField(verbose_name='描述', max_length=64, null=True)

    class Meta:
        table_name = 'pic'


class Video(BaseModel):
    user_id = IntegerField(verbose_name='用户', index=True)
    title = CharField(verbose_name='标题', max_length=32, null=True)
    description = CharField(verbose_name='描述', max_length=64, null=True)
    pic = CharField(verbose_name='视频预览图', max_length=128)
    path = CharField(verbose_name='视频路径', max_length=128)

    class Meta:
        table_name = 'video'



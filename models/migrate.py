#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import pathlib
from models.xlup import db
from peewee_migrate import Router


def migrate(name=None, fake=False):
    """makemigrate

    :param name: 迁移文件名称
    :param fake: fake=True, 如果你的数据库已经有了数据, 且不想删除它
    """
    router = Router(db, ignore='basemodel')
    names = [mm.name for mm in router.model.select().order_by(router.model.id)]
    if name:
        router.run(name, fake)
    else:
        path = pathlib.Path(__file__).parent
        migrations_path = path.joinpath('migrations')
        for single in migrations_path.rglob('*_auto.py'):
            if single.stem not in names:
                router.run(single.stem, fake)


if __name__ == "__main__":
    # migrate(name='001_auto', fake=True)
    migrate()

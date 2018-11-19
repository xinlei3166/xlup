#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import models
from models.xlup import db
from peewee_migrate import Router


def makemigrations(auto=False):
    """database makemigrations

    :param auto: auto=True, run all unapplied migrations
    """
    router = Router(db, ignore='basemodel')
    if auto:
        router.create(auto=models)
    else:
        router.create()


if __name__ == "__main__":
    makemigrations(auto=False)

#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: redis_model.py
@time: 2017/3/24 下午2:06
"""

import json

import redis
from affiliate.model.config import redis as red


class R():
    def __init__(self):
        self._r = redis.Redis(host=red['host'], port=red['port'], db=red['db'], password=red['password'])

    @property
    def r(self):
        return self._r

    def lpush(self, name, *values):
        return self._r.lpush(name, *values)

    def rpop(self, key):
        return self._r.rpop(key)

    def llen(self, key):
        return self._r.llen(key)

    def hset(self, name, key, value):
        return self._r.hset(name, key, value)

    def set(self, key, value):
        return self._r.set(key, value)

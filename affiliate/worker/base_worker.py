#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: base_worker.py
@time: 2017/3/30 下午1:27
"""
from affiliate.model.mysql_model import ThirdPartyOffer


class BaseWorker:
    def __init__(self, taskId, userId, url, username, password):
        self.taskId = taskId
        self.userId = userId
        self.url = url
        self.username = username
        self.password = password

    def delete_old_offers(self):
        ThirdPartyOffer.delete().where(ThirdPartyOffer.taskId == self.taskId).execute()

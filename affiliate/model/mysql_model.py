#!/usr/bin/env python
# encoding: utf-8

from peewee import *
from affiliate.model.config import mysql

db = MySQLDatabase(mysql['name'],
                   host=mysql['host'],
                   port=int(mysql['port']),
                   user=mysql['user'],
                   passwd=mysql['passwd']
                   )


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db


class User(BaseModel):
    idText = CharField(max_length=8, null=False)
    email = CharField(max_length=50, null=False)
    emailVerified = IntegerField(null=False, default=0)
    contact = TextField(null=False)
    password = CharField(max_length=256, null=False, default='')
    firstname = CharField(max_length=256, null=False, default='')
    lastname = CharField(max_length=256, null=False, default='')
    campanyName = CharField(max_length=256, null=False, default='')
    status = IntegerField(null=False, default=0)
    registerts = IntegerField()
    lastLogon = IntegerField()
    timezone = CharField(max_length=6, null=False, default='+00:00')
    timezoneId = IntegerField(null=False)
    rootdomainredirect = CharField(max_length=512, null=False, default='')
    json = TextField(null=False)
    setting = TextField(null=False)
    referralToken = CharField(max_length=128, null=False)
    deleted = IntegerField(null=False, default=0)

    class Meta:
        db_table = "User"
        index = (('idText', True), ('email', True))


class OfferSyncTask(BaseModel):
    """
    task
    """
    userId = IntegerField(null=False)
    thirdPartyANId = IntegerField()
    status = IntegerField(default=0)  # 0:新建;1:运行中;2:出错;3:完成
    executor = CharField(max_length=32, null=False)  # 执行者的唯一标识  mac地址
    message = TextField()
    createdAt = IntegerField(null=False)
    startedAt = IntegerField(null=False)
    endedAt = IntegerField(null=False)
    deleted = IntegerField(null=False, default=0)  # 0:未删除;1:已删除

    class Meta:
        db_table = "OfferSyncTask"


class ThirdPartyAffiliateNetwork(BaseModel):
    """
    affiliate login info
    """
    userId = IntegerField(null=False)
    trustedANId = IntegerField(null=False)  # TemplateAffiliateNetwork
    name = CharField(max_length=256, null=False, default='')
    token = TextField()
    userName = TextField()
    password = TextField()
    createdAt = IntegerField(null=False)
    deleted = IntegerField(null=False, default=0)

    class Meta:
        db_table = "ThirdPartyAffiliateNetwork"


class TemplateAffiliateNetwork(BaseModel):
    """
    provider
    """
    name = CharField(max_length=256, null=False)
    postbackParams = TextField(null=False)  # 回调url中参数的写法:{cid:%subid1%;p:%commission%}
    desc = TextField(null=False)  # 关于该AfflicateNetwork的描述，HTML
    apiOffer = IntegerField(null=False)  # 0:不支持api拉取Offer;1:支持拉取Offer
    apiUrl = TextField(null=False)
    apiMode = IntegerField(null=False)  # 1:仅token;2:仅Username/password;3:token/up都支持
    deleted = IntegerField(null=False, default=0)

    class Meta:
        db_table = "TemplateAffiliateNetwork"


class ThirdPartyOffer(BaseModel):
    """
    offer
    """
    userId = IntegerField(null=False)
    taskId = IntegerField(null=False)
    status = IntegerField(null=False)
    offerId = TextField()
    name = CharField(max_length=256, null=False, default='')
    previewLink = TextField()
    trackingLink = TextField()
    countryCode = TextField()
    payoutMode = IntegerField(null=False, default=1)
    payoutValue = DecimalField(null=False, default='0.00000')
    category = TextField()
    carrier = TextField()
    platform = TextField()
    detail = TextField()

    class Meta:
        db_table = "ThirdPartyOffer"


class Country(BaseModel):
    name = CharField(max_length=256, null=False)
    alpha2Code = CharField(max_length=2, null=False)
    alpha3Code = CharField(max_length=3, null=False)
    numCode = IntegerField(null=False)

    class Meta:
        db_table = "Country"
        index = (('alpha2Code', True), ('alpha3Code', True), ('numCode', True))


db.connect()

# a = Country.update(name='ccc').where(Country.id == 1).execute()
# pass

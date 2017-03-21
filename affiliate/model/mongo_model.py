from mongoengine import *
from affiliate.model.config import mongodb

connect(mongodb['name'], host=mongodb['host'], port=int(mongodb['port']))


class Provider(Document):
    name = StringField(required=True)

    @classmethod
    def get_or_create(cls, name):
        obj = cls.objects.filter(name=name)
        return obj[0] if obj else cls.objects.create(name=name)


class ApiToken(Document):
    mode = BooleanField()
    token = StringField()
    username = StringField()
    password = StringField()
    user_id = StringField()
    provider_id = StringField(required=True)

    @classmethod
    def get_or_create(cls, token, provider_id, username, user_id, mode, password=''):
        obj = cls.objects.filter(token=token, provider_id=provider_id, username=username, password=password,
                                 user_id=user_id, mode=mode)
        return obj[0] if obj else cls.objects.create(token=token, provider_id=provider_id, username=username,
                                                     password=password,
                                                     user_id=user_id, mode=mode)


class Affiliates(Document):
    name = StringField()
    banner = StringField()
    provider_id = StringField(required=True)
    api_token = StringField(required=True)
    carriers = StringField()
    country = ListField()
    offer_id = StringField(required=True)
    payout = StringField(required=True)
    preview_link = StringField()
    tracking_link = StringField(required=True, unique=True)

    @classmethod
    def save_all(cls, data):
        [cls.objects.create(**item) for item in data]


from mongoengine import *
from affiliate.model.config import mongodb

connect(mongodb['name'], host=mongodb['host'], port=int(mongodb['port']))


class MCampaignStatistics(Document):
    provider_id = IntField(required=True)
    date = DateTimeField(required=True)
    raw = DictField(required=True)



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


class AProvider(BaseModel):
    name = CharField(null=False)

    class Meta:
        db_table = "providers"
        indexes = (
            (('name'), True),  # the index should be unique.
        )


class AApiToken(BaseModel):
    model = BooleanField(max_length=255, null=False)
    token = CharField(null=False)
    username = CharField()
    password = CharField()
    userId = CharField()
    # initialized = BooleanField(default=False)
    provider = ForeignKeyField(AProvider)

    # provider=ForeignKeyField(AProvider,related_name='id')

    class Meta:
        db_table = "api_tokens"
        indexes = (
            (('token', 'username', 'password', 'userId', 'provider'), True),
            # (('token', 'username', 'password', 'userId','provider_id'), True),
        )


class AAffiliates(BaseModel):
    name = CharField(null=False)
    affiliate_identity = CharField(null=False)
    provider = ForeignKeyField(AProvider)
    api_token = ForeignKeyField(AApiToken)

    class Meta:
        db_table = "affiliates"

    indexes = (
        (('provider', 'affiliate_identity'), True),
        # (('provider_id', 'affiliate_identity'), True),
    )


class AStatistics(BaseModel):
    carriers = CharField()
    countries = TextField()
    category = CharField()
    conversion_flow = CharField()
    exclusive = CharField()
    offer_description = TextField()
    offer_type = CharField()
    payout = CharField()
    preview_url = CharField()
    tracklink = CharField()

    provider = ForeignKeyField(AProvider)
    affiliate = ForeignKeyField(AAffiliates)
    api_token = ForeignKeyField(AApiToken)

    class Meta:
        db_table = "statistics"

    indexes = (
        ('affiliate_id', 'payout', 'conversion_flow', 'offer_type', 'provider_id', 'api_token_id', 'tracklink'), True)


db.connect()

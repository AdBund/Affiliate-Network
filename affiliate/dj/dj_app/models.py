from __future__ import unicode_literals

from django.db import models


# Create your models here.

class AProvider(models.Model):
    name = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = "providers"
        unique_together = ('name',)


class AApiToken(models.Model):
    mode = models.BooleanField(max_length=255, default=False)
    token = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    userId = models.CharField(max_length=255, null=True)
    # initialized = BooleanField(default=False)
    provider = models.ForeignKey(AProvider)

    # provider=ForeignKeyField(AProvider,related_name='id')

    class Meta:
        db_table = "api_tokens"
        unique_together = [('token', 'username', 'password', 'userId', 'provider')]


class AAffiliates(models.Model):
    name = models.CharField(max_length=255, null=False)
    affiliate_identity = models.CharField(max_length=255, null=False)
    provider = models.ForeignKey(AProvider)
    api_token = models.ForeignKey(AApiToken)

    class Meta:
        db_table = "affiliates"

        unique_together = ('provider', 'affiliate_identity')


class AStatistics(models.Model):
    carriers = models.CharField(max_length=255, null=True)
    countries = models.TextField(null=True)
    category = models.CharField(max_length=255, null=True)
    conversion_flow = models.CharField(max_length=255, null=True)
    exclusive = models.CharField(max_length=255, null=True)
    offer_description = models.TextField(null=True)
    offer_type = models.CharField(max_length=255, null=True)
    payout = models.CharField(max_length=255, null=True)
    preview_url = models.CharField(max_length=255, null=True)
    tracklink = models.CharField(max_length=255, null=True)

    provider = models.ForeignKey(AProvider)
    affiliate = models.ForeignKey(AAffiliates)
    api_token = models.ForeignKey(AApiToken)

    class Meta:
        db_table = "statistics"

        unique_together = (
            'affiliate', 'payout', 'conversion_flow', 'offer_type', 'provider', 'api_token', 'tracklink')

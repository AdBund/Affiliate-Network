# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AAffiliates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('affiliate_identity', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'affiliates',
            },
        ),
        migrations.CreateModel(
            name='AApiToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('userId', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'api_tokens',
            },
        ),
        migrations.CreateModel(
            name='AProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'providers',
            },
        ),
        migrations.CreateModel(
            name='AStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriers', models.CharField(max_length=255, null=True)),
                ('countries', models.CharField(max_length=255, null=True)),
                ('category', models.CharField(max_length=255, null=True)),
                ('conversion_flow', models.CharField(max_length=255, null=True)),
                ('exclusive', models.CharField(max_length=255, null=True)),
                ('offer_description', models.TextField(null=True)),
                ('offer_type', models.CharField(max_length=255, null=True)),
                ('payout', models.CharField(max_length=255, null=True)),
                ('preview_url', models.CharField(max_length=255, null=True)),
                ('tracklink', models.CharField(max_length=255, null=True)),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_app.AAffiliates')),
                ('api_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_app.AApiToken')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_app.AProvider')),
            ],
            options={
                'db_table': 'statistics',
            },
        ),
        migrations.AlterUniqueTogether(
            name='aprovider',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='aapitoken',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_app.AProvider'),
        ),
        migrations.AddField(
            model_name='aaffiliates',
            name='api_token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_app.AApiToken'),
        ),
        migrations.AddField(
            model_name='aaffiliates',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_app.AProvider'),
        ),
        migrations.AlterUniqueTogether(
            name='astatistics',
            unique_together=set([('affiliate', 'payout', 'conversion_flow', 'offer_type', 'provider', 'api_token', 'tracklink')]),
        ),
        migrations.AlterUniqueTogether(
            name='aapitoken',
            unique_together=set([('token', 'username', 'password', 'userId', 'provider')]),
        ),
        migrations.AlterUniqueTogether(
            name='aaffiliates',
            unique_together=set([('provider', 'affiliate_identity')]),
        ),
    ]

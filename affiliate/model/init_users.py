#!/usr/bin/env python
# encoding: utf-8

"""
初始化用户
"""

from affiliate.model.mongo_model import Provider, ApiToken

if __name__ == '__main__':
    yeahmobi = Provider.get_or_create(name="yeahmobi")
    avazu = Provider.get_or_create(name="avazu")
    ApiToken.get_or_create(token='67951dc0eec37c70b7cc33bfb9b1435d',
                           provider_id=str(yeahmobi.id),
                           username='dsp@jetmobo.com',
                           password='Ihave2cars$',
                           user_id='71',
                           mode=True)
    ApiToken.get_or_create(token='23011', provider_id=str(avazu.id), username='18629', user_id='71', mode=False)
    ApiToken.get_or_create(token='22433', provider_id=str(avazu.id), username='18629', user_id='71', mode=False)
    ApiToken.get_or_create(token='22417', provider_id=str(avazu.id), username='18629', user_id='71', mode=False)
    ApiToken.get_or_create(token='22416', provider_id=str(avazu.id), username='18629', user_id='71', mode=False)

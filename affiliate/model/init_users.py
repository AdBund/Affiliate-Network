#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: init_users.py
@time: 2017/3/17 下午2:20
"""

"""
初始化用户
"""

from affiliate.model.mysql_model import AProvider, AApiToken, AAffiliates, AStatistics, db

if __name__ == '__main__':
    yeahmobi = AProvider.get_or_create(name="yeahmobi")
    avazu = AProvider.get_or_create(name='avazu')
    AApiToken.get_or_create(token='67951dc0eec37c70b7cc33bfb9b1435d',
                            provider=yeahmobi[0],
                            username='dsp@jetmobo.com',
                            password='Ihave2cars$',
                            userId='71')
    AApiToken.get_or_create(token='23011', provider=avazu[0], username='18629', userId=71)
    AApiToken.get_or_create(token='22433', provider=avazu[0], username='18629', userId=71)
    AApiToken.get_or_create(token='22417', provider=avazu[0], username='18629', userId=71)
    AApiToken.get_or_create(token='22416', provider=avazu[0], username='18629', userId=71)

#!/usr/bin/env python
# encoding: utf-8

"""
@author: amigo
@contact: 88315203@qq.com
@phone: 15618318407
@software: PyCharm
@file: load_yaml.py
@time: 2017/3/20 下午1:15
"""
import os
import yaml
from jsonpath_rw import jsonpath, parse, Parent
from affiliate.model.mongo_model import Provider, ApiToken, Affiliates
from affiliate.rest.yeahmobi import Yeahmobi


class LoadYaml():
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # path = os.path.join(base_dir, 'config\config.yaml')
        path = os.path.join(base_dir, 'config\yeahmobi_config.yaml')
        if not os.path.exists(path):
            raise Exception('config file not exit')
        f = open(path)
        self.y = yaml.load(f)

    def get_login_params(self):
        return self.y['login']

    def data_processing(self, data, api_token):
        login = self.y['login']
        affiliate = self.y['affiliate']
        provider_name = login['provider']
        provider = Provider.objects.get(name=provider_name)
        loop_path = affiliate['loop_path']
        contents = affiliate['contents']
        save_data = []


        if isinstance(parse(loop_path).find(data)[0].value, dict):
            self.offer_dict(api_token, contents, data, loop_path, provider, save_data)
        if isinstance(parse(loop_path).find(data)[0].value, list):
            self.offerId_list(api_token, contents, data, loop_path, provider, save_data)

            # for k, v in dict(parse(loop_path).find(data)[0].value).items():
            #     print(k)
            # print(k, v)

    def offer_dict(self, api_token, contents, data, loop_path, provider, save_data):
        for k, v in dict(parse(loop_path).find(data)[0].value).items():
            tmp = {}
            tmp['provider_id'] = str(provider.id)
            tmp['api_token'] = str(api_token)

            if 'offer_id' not in contents:
                tmp['offer_id'] = str(k)
            for content in contents:
                element_keywords = contents[content]

                if '_ _ ' not in element_keywords:
                    tmp[content] = v[element_keywords]


                # if ('_ _ ' in element_keywords) and ('*' not in element_keywords):
                #     first_parent = Parent().find(Parent().find(v)[0])[0]
                #     element_keywords = element_keywords[4:]
                #     tmp[content] = first_parent.value[element_keywords]  # todo :error:if ont find
                #
                # if '_ _ ' in content and ' * ' in content:
                #     first_parent = Parent().find(Parent().find(v)[0])[0]
                #     nPos = element_keywords.index('*')
                #     element_keywords = element_keywords[4:nPos - 1]
                #     element_parent = element_keywords
                #     element_child = element_keywords[(nPos + 2):]
                #     parent_lists = first_parent.value[element_parent]
                #
                #     parent_l_array = []
                #     for parent_l in parent_lists:
                #         parent_l_array.append(parent_l.value[element_child])
                #
                #     tmp[element_child] = parent_l_array
                #     # todo :1.th same one ;2.diff one

                # country array
                if 'country' in tmp:
                    country = tmp['country']
                    if isinstance(country, str):
                        # todo:
                        tmp['country'] = [tmp['country']]
                if 'offer_id' in tmp:
                    tmp['offer_id'] = str(tmp['offer_id'])
                if 'payout' in tmp:
                    tmp['payout'] = str(tmp['payout'])

            save_data.append(tmp)
        print(save_data)
        print('end')
        # return save_data



    def offerId_list(self, api_token, contents, data, loop_path, provider, save_data):
        print('###########')
        for loop in parse(loop_path).find(data):
            print('----------------')
            tmp = {}
            tmp['provider_id'] = str(provider.id)
            tmp['api_token'] = str(api_token)

            for content in contents:
                element_keywords = contents[content]

                if '_ _ ' not in element_keywords:
                    tmp[content] = loop.value[element_keywords]

                if ('_ _ ' in element_keywords) and ('*' not in element_keywords):
                    first_parent = Parent().find(Parent().find(loop)[0])[0]
                    element_keywords = element_keywords[4:]
                    tmp[content] = first_parent.value[element_keywords]  # todo :error:if ont find

                if '_ _ ' in content and ' * ' in content:
                    first_parent = Parent().find(Parent().find(loop)[0])[0]
                    nPos = element_keywords.index('*')
                    element_keywords = element_keywords[4:nPos - 1]
                    element_parent = element_keywords
                    element_child = element_keywords[(nPos + 2):]
                    parent_lists = first_parent.value[element_parent]

                    parent_l_array = []
                    for parent_l in parent_lists:
                        parent_l_array.append(parent_l.value[element_child])

                    tmp[element_child] = parent_l_array
                    # todo :1.th same one ;2.diff one

                # country array
                if 'country' in tmp:
                    country = tmp['country']
                    if isinstance(country, str):
                        # todo:
                        tmp['country'] = [tmp['country']]
                if 'offer_id' in tmp:
                    tmp['offer_id'] = str(tmp['offer_id'])
                if 'payout' in tmp:
                    tmp['payout'] = str(tmp['payout'])

            save_data.append(tmp)
        print(save_data)
        print('end')
        # return save_data




def parse_content(self, key, data):
    content = self.y['content']
    levels = content[key]
    ret = data.get(levels, '')
    return ret


if __name__ == '__main__':
    avazu = {'campaigns': [{
        'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201505\\/098\\/e62dca38e59753c18fd831dc096ede0f.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201505\\/023\\/bbf2368ee99e4600cd4a7ba673cfca29.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/114\\/3552018890dc864b9b758c8b7857fa45.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/122\\/9d730fe3c9d15a999bbf64d115ac48da.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/031\\/eed2f827d96ad5ce8d6eb7afc0528879.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/108\\/e5f1d3da1cee7f894c7a987e8f6a3d5d.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/096\\/ed87d10ce74c845daf937bd20ab01c73.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/031\\/833cb72da6e496ebf42cce700db083a0.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201505\\/023\\/bbf2368ee99e4600cd4a7ba673cfca29.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201510\\/038\\/68a329461bfc0fa741cf3f8050732c7b.zip"]',
        'carrier': 'WIFI,All Poland Carriers', 'category': '107', 'conntype': '1,2',
        'convflow': '108', 'cpnid': 9342, 'cpnname': 'Xtubes Poland Mobile(Adult)',
        'description': 'Carrier%3A+Carrier%3A+PLUS+3G+%28one-click-sale%29+%26+Orange%2CWi-Fi+%28MT+flow%29%0D%0A%0D%0ARestriction%3A%0D%0ANo+incent%0D%0ANo+adult%0D%0ANo+misleading%0D%0A%0D%0AAsk+for+the+ip+targeted+lists+from+your+AM+if+necessary',
        'devicetype': '1', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 21043, 'lpname': 'Xtube V4 PL', 'payout': 6.0, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=mTeueOjMIWuXeW45KNeXD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 195681, 'lpname': 'xTubesV19 PL', 'payout': 6.0, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=mTeueOjMIWuXeToQKWJngTuwD3jReUbneG-0N-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 195683, 'lpname': 'xTubesV21 PL', 'payout': 6.0, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=mTeueOjMIWuXeToQKWJUgTuwD3jReUbneG-0N-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 195684, 'lpname': 'xTubesV23 PL', 'payout': 6.0, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=mTeueOjMIWuXeToQKWJugTuwD3jReUbneG-0N-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 195686, 'lpname': 'BikiniBayV7 PL', 'payout': 6.0, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=mTeueOjMIWuXeToQKWJHgTuwD3jReUbneG-0N-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 832984, 'lpname': 'xTubesV19 PL', 'payout': 6.0, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=mTeueOjMIWuXmNeRmTJugTuwD3jReUbneG-0N-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
        'minosv': '0.0', 'os': '1,2', 'policy': 1,
        'traffictype': '111,105,110,102,101,103,104,108'}, {
        'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201511\\/002\\/dd34279b19a31bed7fa54df0650285f7.zip"]',
        'carrier': 'India_Airtel', 'category': '107', 'conntype': '1,2', 'convflow': '108',
        'cpnid': 220841, 'cpnname': 'Airtel Follo Mobile India(Adult)',
        'description': 'Update%3A+All+traffic+allowed+EXCEPT+Facebook+Traffic%0D%0A%0D%0ARestriction%3A%0D%0ANo+Facebook+Traffic%0D%0AAdult+Traffic+Allowed%0D%0A%0D%0APreview%3A%0D%0Ahttp%3A%2F%2Fpromo.adz2lead.com%2Fappsoftheday%2F',
        'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 236491, 'lpname': 'Airtel Follo Mobile IN (Adult)', 'payout': 0.49, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW25mNGngTuwD3jReU9umT4XD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
        'minosv': '0.0', 'os': '1,2', 'policy': 1,
        'traffictype': '111,112,105,110,102,106,107,101,103,104,108'}, {
        'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201511\\/065\\/87d035944d75455bbd448e04b5dac7f0.zip"]',
        'carrier': 'India_Vodafone', 'category': '101,107', 'conntype': '1,2', 'convflow': '108',
        'cpnid': 221022, 'cpnname': 'Vodafone Video Club Mobile India(Adult)(Incent)',
        'description': 'Restriction%3A%0D%0ANo+Facebook+Traffic%0D%0Asocial+network+traffic+is+not+allowed.%0D%0A%0D%0APreview%3A%0D%0Ahttp%3A%2F%2Fpromo.adz2lead.com%2Fappsoftheday%2F',
        'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 236669, 'lpname': 'Vodafone Video Club Mobile IN (Adult)', 'payout': 0.6,
             'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW2neN2RgTuwD3jReU9HKWoXD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
        'minosv': '0.0', 'os': '1,2', 'policy': 1,
        'traffictype': '111,112,105,110,109,102,106,107,101,103,104,108'}, {
        'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201511\\/127\\/e003b80d731de8852163fd87dfc9e955.zip"]',
        'carrier': 'India_IDEA', 'category': '107', 'conntype': '1,2', 'convflow': '108',
        'cpnid': 221051, 'cpnname': 'Idea Video Club Mobile India Incent(Adult)',
        'description': 'Update%3A+Pub+payout+increased+from+%240.4+to+%240.42.+Take+effect+immediately.++++Update%3AAll+traffic+allowed+EXCEPT+Facebook+Traffic++++Restriction%3A++No+Facebook+Traffic++Adult+Traffic+Allowed++++Preview%3A++http%3A%2F%2Fpromo.adz2lead.com%2Fappsoftheday%2F',
        'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 236681, 'lpname': 'Idea Video Club Mobile IN(Adult)(Incent)', 'payout': 0.42,
             'pkgname': '', 'previewlink': 'http://promo.adz2lead.com/appsoftheday/',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW2neNjngTuwD3jReU9HmN4XD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
        'minosv': '0.0', 'os': '1,2', 'policy': 1,
        'traffictype': '111,112,105,110,102,106,107,101,103,104,108'}, {
        'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201511\\/054\\/914369910effb38878b1b3a9f2020cdf.zip"]',
        'carrier': 'India_BSNL', 'category': '107', 'conntype': '1,2', 'convflow': '108',
        'cpnid': 221091, 'cpnname': 'Bsnl Babes Club Mobile India Incent(Adult)',
        'description': 'Update%3A+Pub+payout+increased+from+%240.27+to+%240.3.+Take+effect+immediately.++++Adult+Traffic+Allowed++No+Facebook+Traffic++++Preview%3A++http%3A%2F%2Fpromo.adz2lead.com%2Fappsoftheday%2F',
        'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
             'enforcedv': '', 'lpid': 236720, 'lpname': 'Bsnl Babes Club Mobile IN (Adult)(Incent)', 'payout': 0.3,
             'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW2neNongTuwD3jReU90eWbXD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
        'minosv': '0.0', 'os': '1,2', 'policy': 1,
        'traffictype': '111,112,105,110,102,106,107,101,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,Malaysia_DiGi,Malaysia_U Mobile', 'category': '107',
         'conntype': '1,2', 'convflow': '103', 'cpnid': 594255,
         'cpnname': 'Slamdjam Malaysia Mobile(Incent)',
         'description': 'Open+cap%21%0D%0A%0D%0A-+No+Fraud%0D%0A-+No+adult%0D%0A-+No+misleading%0D%0A-+No+usage+of+word+free%2C+no+carrier+names%2C+no+WIN+on+download+offer',
         'devicetype': '1', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'MY', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 687533,
             'lpname': 'Antivirus MY (Digi/ U-Mobile)(Incent)', 'payout': 3.0, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=KToueWjQgTuwD3jHmN8QeUeXD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'MY', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 845549,
             'lpname': 'Download 2 MY (Incent)(Digi/ U-Mobile)', 'payout': 3.0, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=KToueWjQgTuwD3jrKNjQKNoXD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'MY', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 845552,
             'lpname': 'Download 1 MY (Incent)(Digi/ U-Mobile)', 'payout': 3.0, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=KToueWjQgTuwD3jrKNjQKT2XD3xMgT2UeN4n&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'MY', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2604462,
             'lpname': 'Download 3 MY (Incent)(Digi/ U-Mobile)', 'payout': 3.0, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=KToueWjQgTuwD3jRKWbuKN9RgTuwD3jReUbneG-0N-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1,
         'traffictype': '112,110,109,102,106,107,101,113,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,Iraq_AsiaCell,Iraq_Korek Telecom,Iraq_Zain Iraq',
         'category': '107', 'conntype': '1,2', 'convflow': '106', 'cpnid': 1172713,
         'cpnname': 'Karamblam Iraq Mobile(MT Flow)',
         'description': 'Open+cap%21%0D%0A%0D%0ANo+incent+traffic%0D%0ANo+fraud+traffic%0D%0ANo+adult+traffic%0D%0ANo+whatsapp+traffic%0D%0ANo+usage+of+word+free%2C+no+carrier+names%2C+no+WIN+on+download+offer%0D%0A%0D%0APreview+link%3A%0D%0A-+Download%09%0D%0Ahttp%3A%2F%2Furoffer.link%2Fnew%3Fservice%3DRnVtYmxv%26country%3DIQ%26reffid%3Dba5f00b6e91db6cfc2804db9cadf721c%26networkid%3D333%26optinfo%3Dclickid%26publisher%3Daffiliateid+%0D%0A-+Whatsapp%0D%0Ahttp%3A%2F%2Furoffer.link%2Fnew%3Fservice%3DRnVtYmxv%26country%3DIQ%26reffid%3D4200efaea9d5fbbc9ace86f486040f35%26networkid%3D333%26optinfo%3Dclickid%26publisher%3Daffiliateid%0D%0A-+AV%0D%0Ahttp%3A%2F%2Furoffer.link%2Fnew%3Fservice%3DRnVtYmxv%26country%3DIQ%26reffid%3D564c2e6434f7a3376031c01619c2be27%26networkid%3D333%26optinfo%3Dclickid%26publisher%3Daffiliateid',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IQ', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2142914,
             'lpname': 'Download IQ', 'payout': 1.15, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT40eW8neRjMIWuXeW4ueWonKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'IQ', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3350511,
             'lpname': 'Whatsapp IQ', 'payout': 1.15, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT40eW8neRjMIWuXeUeQeNjne3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'IQ', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3350534,
             'lpname': 'Antivirus IQ', 'payout': 1.15, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT40eW8neRjMIWuXeUeQeNjUKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,110,109,101,113,104,108'},
        {'banner': '[]', 'carrier': 'Mexico_Telcel', 'category': '107', 'conntype': '2',
         'convflow': '111', 'cpnid': 1325326, 'cpnname': 'Kmbajo Club Sexy Mexico 2 Click',
         'description': 'No+Fraud', 'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'MX', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1421931,
             'lpname': 'Sexy Black MX ', 'payout': 2.7, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTeRKTeRKOjMIWuXeTGReToUe3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'MX', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1421933,
             'lpname': 'Sexy Light MX', 'payout': 2.7, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTeRKTeRKOjMIWuXeTGReToUeRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'MX', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1421934,
             'lpname': 'Sexy Playa MX', 'payout': 2.7, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTeRKTeRKOjMIWuXeTGReToUKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'MX', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1421938, 'lpname': 'Amm MX ',
             'payout': 2.7, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTeRKTeRKOjMIWuXeTGReToUmzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '111,112,109,101'},
        {'banner': '[]', 'carrier': 'WIFI,Guatemala_Claro,Guatemala_Tigo', 'category': '107',
         'conntype': '1,2', 'convflow': '108', 'cpnid': 1499288,
         'cpnname': 'Sexy Jamba Mobile Guatemala(One Click)',
         'description': 'No+Incent%0D%0ANo+Fraud%0D%0A%0D%0AOperator+TIGO+Only', 'devicetype': '1,2',
         'lps': [{'city': '', 'cityinclude': 2, 'country': 'GT', 'countryinclude': 1,
                  'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1599114,
                  'lpname': 'Chicas GT (Tigo Only)', 'payout': 0.58, 'pkgname': '', 'previewlink': '',
                  'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTGamT2rmzjMIWuXeTjamT4nKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
                 {'city': '', 'cityinclude': 2, 'country': 'GT', 'countryinclude': 1,
                  'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1599225,
                  'lpname': 'Chicas GT (Claro Only)', 'payout': 0.58, 'pkgname': '', 'previewlink': '',
                  'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTGamT2rmzjMIWuXeTjamT2RK3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,109,101,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,Honduras_Claro,Honduras_Tigo', 'category': '107',
         'conntype': '1,2', 'convflow': '108', 'cpnid': 1499673,
         'cpnname': 'Sexy Jamster Mobile Honduras(One Click)',
         'description': 'No+Incent%0D%0ANo+Fraud', 'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'HN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1599511,
             'lpname': 'Chicas HN (Tigo Only)', 'payout': 0.58, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTGamT90eRjMIWuXeTjamTjne3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'HN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1599512,
             'lpname': 'Chicas HN (Claro Only)', 'payout': 0.58, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eTGamT90eRjMIWuXeTjamTjneOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '111,101,104'}, {
            'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201612\\/016\\/4b7c30088880a197ffbab1876a14233a.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201612\\/077\\/512d7ee49d1c020d536469e0f30729ba.zip"]',
            'carrier': 'WIFI,Saudi Arabia_STC', 'category': '107', 'conntype': '1,2',
            'convflow': '103', 'cpnid': 1788686, 'cpnname': 'StarzPlayz Saudi Arabia(STC and wifi)',
            'description': 'No+Fraud%0D%0ANo+incent%0D%0ANo+adult%0D%0A%0D%0ATargeting%3A%0D%0ASTC+Only%0D%0AWifi+accepted',
            'devicetype': '1,2', 'lps': [
                {'city': '', 'cityinclude': 2, 'country': 'SA', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 1932978, 'lpname': 'StarzPlay SA (Arabic)', 'payout': 21.0, 'pkgname': '',
                 'previewlink': 'https://arabia.starzplay.com/ar/partners/stc-saudi?utm_source=affiliate&utm_term=general&utm_medium=banner&utm_campaign=avz&a_bid=47a71cd1&utm_content={vurl}&data2={avazu_id}',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8rmN9rKOjMIWuXeToUeWo0mzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
                {'city': '', 'cityinclude': 2, 'country': 'SA', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 2158333, 'lpname': 'StarzPlay SA (English)', 'payout': 21.0, 'pkgname': '',
                 'previewlink': 'https://arabia.starzplay.com/en/partners/stc-saudi?utm_source=affiliate&utm_term=general&utm_medium=banner&utm_campaign=avz&a_bid=47a71cd1&utm_content={vurl}&data2={avazu_id}',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8rmN9rKOjMIWuXeW4QmNeUeRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
            'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,110,109,101,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,Kuwait_Ooredoo', 'category': '107', 'conntype': '1,2',
         'convflow': '103', 'cpnid': 1788739, 'cpnname': 'StarzPlay Kuwait(Ooredoo and wifi)',
         'description': 'No+fraud%0D%0ANo+adult%0D%0ANo+incent%0D%0ACarrier%3A+Ooredoo%0D%0A%0D%0ATargeting%3A%0D%0AOoredoo+Only%0D%0AWifi+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'KW', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 1933002,
             'lpname': 'StarzPlay KW (Arabic)', 'payout': 21.0, 'pkgname': '',
             'previewlink': 'https://arabia.starzplay.com/ar/partners/ooredoo-kuwait?utm_source=affiliate&utm_term=general&utm_medium=banner&utm_campaign=avz&a_bid=47a71cd1&utm_content={vurl}&data2={avazu_id}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8rmN8Um3jMIWuXeToUeUb5eOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'KW', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2158384,
             'lpname': 'StarzPlay KW (English)', 'payout': 21.0, 'pkgname': '',
             'previewlink': 'https://arabia.starzplay.com/en/partners/ooredoo-kuwait?utm_source=affiliate&utm_term=general&utm_medium=banner&utm_campaign=avz&a_bid=47a71cd1&utm_content={vurl}&data2={avazu_id}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8rmN8Um3jMIWuXeW4QmNerKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,110,109,101,104,108'}, {
            'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201610\\/068\\/344fb76c813c36769d04c525cac90b9d.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201610\\/102\\/8a4def276b51396477815c035158450c.zip","http:\\/\\/cdn.avazu.net\\/zips\\/201610\\/032\\/a0c1d771ec549be0156c302d02abc8d9.zip"]',
            'carrier': 'WIFI,All Carrier Network Traffic', 'category': '109', 'conntype': '1,2',
            'convflow': '110', 'cpnid': 1790221, 'cpnname': 'Want to Win France Mobile(SOI)(Capped)',
            'description': 'Accepted+traffic+sources%3A+Email+%2F+Pop+%2F+%28in+App%29+Display+%2F+Redirect+%2F+Social+%2F+Google+%2F+Search+%2F+Wifi+%2F+3g+%2F+SMS%0D%0ADenied+traffic+sources%3A+Whatsapp+Virals+%2F+Social+Virals+%2F+Content+Lock+%2F+Adult+%2F+incentivized+%2F+Virtual+currency%0D%0AAll+offers+are+responsive.%0D%0AAggressive+prelanders+are+allowed.%0D%0APrefilling+is+possible+with+the+next+parameters%3A+%0D%0Agender%3Dfemale%26fname%3DTest%26lname%3DTester%26email%3Dwa%40hotmail.com%26bday%3D04%26bmonth%3D05%26byear%3D1990%0D%0A%0D%0A%0D%0ANo+Fraud%0D%0ANo+Adult%0D%0ANo+iframing',
            'devicetype': '1,2', 'lps': [
                {'city': '', 'cityinclude': 2, 'country': 'FR', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 1935185, 'lpname': 'iPhone7 FR', 'payout': 0.6, 'pkgname': '',
                 'previewlink': 'http://lp.want-to-win.com/fr/iphone7/?networkid=1&optinfo=XXXX&publisher=XXXX',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8aeN2Re3jMIWuXeToUKT4rK3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
                {'city': '', 'cityinclude': 2, 'country': 'FR', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 1935187, 'lpname': 'Carrefour FR', 'payout': 0.6, 'pkgname': '',
                 'previewlink': 'http://lp.want-to-win.com/fr/supermarket01/?networkid=1&optinfo=XXXX&publisher=XXXX',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8aeN2Re3jMIWuXeToUKT4rKRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
                {'city': '', 'cityinclude': 2, 'country': 'FR', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 1935188, 'lpname': 'Aldi FR', 'payout': 0.6, 'pkgname': '',
                 'previewlink': 'http://lp.want-to-win.com/fr/supermarket02/?networkid=1&optinfo=XXXX&publisher=XXXX',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eT8aeN2Re3jMIWuXeToUKT4rmzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
            'minosv': '0.0', 'os': '1,2', 'policy': 1,
            'traffictype': '112,105,110,109,102,101,113,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,Bulgaria_M-Tel BG', 'category': '107', 'conntype': '1,2',
         'convflow': '103', 'cpnid': 1933647, 'cpnname': 'CellMaxx Bulgaria Mobile',
         'description': 'No+Fraud+Traffic', 'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'BG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2089156,
             'lpname': 'Whatsapp BG ', 'payout': 1.4, 'pkgname': '',
             'previewlink': 'http://celmaxx.com/page?cam=575&country=bg&pub=66&clickid=1477947025mb85646008503',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eToUeU9uKRjMIWuXeWbrmT4QKOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'BG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2265518,
             'lpname': 'Antivirus BG (click2sms)', 'payout': 1.4, 'pkgname': '',
             'previewlink': 'http://celmaxx.com/page?cam=579&country=bg&pub=47&subid={avazu_id}&pubid={vurl}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eToUeU9uKRjMIWuXeW2HKTjnmzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,106,107,101,103,104,108'},
        {'banner': '[]', 'carrier': 'South Africa_VodaCom', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 1943160, 'cpnname': 'Glamour South Afica Mobile(VodaCom Only)',
         'description': 'Only+Andriod+.%0D%0ANo+incent+%0D%0ANo+adult%0D%0ACarrier%3AVodacom.%0D%0APreview%3A%0D%0Ahttp%3A%2F%2F162.243.217.139%2FCC%2FZAGlam%2Findex.php%0D%0AYou+can+use+your+own+banners',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ZA', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2098839,
             'lpname': 'Glamour ZA', 'payout': 4.0, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/ZAGlam/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eToueU4HezjMIWuXeWbamNJUm3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Bangladesh_Grameenphone', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 1943173,
         'cpnname': 'Glamour bangladesh Mobile(Grameenphone Only)',
         'description': 'Only+Andriod+.%0D%0ANo+incent+%0D%0ANo+adult%0D%0ACarrier%3AGrameenphone.%0D%0APreview%3A%0D%0Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fbg%2Findex.php%0D%0AYou+can+use+your+own+banners',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'BD', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2098842,
             'lpname': 'Glamour BD', 'payout': 0.2, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/bg/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eToueU40eRjMIWuXeWbamNJueOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Egypt_Vodafone', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 1943176, 'cpnname': 'Glamour Egypt Mobile(Vodafone Only)',
         'description': 'Only+Andriod+.%0D%0ANo+incent+%0D%0ANo+adult%0D%0ACarrier%3AVodafone%0D%0APreview%3A%0D%0Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fegglm%2Findex.php%0D%0AYou+can+use+your+own+banners',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'EG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2098971,
             'lpname': 'Glamour EG', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/egglm/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eToueU40KOjMIWuXeWbamNo0e3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'All Carrier Network Traffic', 'category': '107',
         'conntype': '1,2', 'convflow': '108', 'cpnid': 1943304,
         'cpnname': 'Glamour Netherlands Mobile',
         'description': 'Only+Andriod+.%0D%0ANo+incent+%0D%0ANo+adult%0D%0Aall+carriers+%2C+but+no+wifi.%0D%0APreview%3A%0D%0Ahttp%3A%2F%2F162.243.217.139%2FCC%2FNL%2Findex.php%0D%0AYou+can+use+your+own+banners',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'NL', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2099001,
             'lpname': 'Glamour NL', 'payout': 5.0, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/NL/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eToueUe5KzjMIWuXeWbamTb5e3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,All Slovakia Carriers', 'category': '107', 'conntype': '1,2',
         'convflow': '105', 'cpnid': 2097882, 'cpnname': 'Vovivooo Slovakia Mobile',
         'description': 'No+Fraud', 'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'SK', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2269904,
             'lpname': 'Antivirus SL (click2sms)', 'payout': 3.8, 'pkgname': '',
             'previewlink': 'http://vovivooo.com/page?cam=579&country=si&pub=47&subid={avazu_id}&pubid={vurl}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWbaKUJreOjMIWuXeW2HmTo5KzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,106,107,101,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,All Serbia Carriers', 'category': '107', 'conntype': '1,2',
         'convflow': '105', 'cpnid': 2097903, 'cpnname': 'Xiomnia Serbia Mobile',
         'description': 'No+Fraud', 'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'RS', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2269929,
             'lpname': 'Antivirus RS (click2sms)', 'payout': 3.0, 'pkgname': '',
             'previewlink': 'http://xiomnia.com/page?cam=545&country=rs&pub=47&subid={avazu_id}&pubid={vurl}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWbaKUo5eRjMIWuXeW2HmToRm3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,106,107,101,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,All Hungary Carriers', 'category': '107', 'conntype': '1,2',
         'convflow': '105', 'cpnid': 2097914, 'cpnname': 'Mobl Apps Hungary Mobile',
         'description': 'Geo%3A+HU%0D%0A%0D%0ARestrictions%3A%0D%0ANo+incent%0D%0ANo+adult%0D%0ANo+social+media+hacking+websites%0D%0ANo+whatsApp+spam%0D%0ANo+email%0D%0ANo+naming+of+operator+in+prelander',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'HU', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2269939,
             'lpname': 'Antivirus HU', 'payout': 9.0, 'pkgname': '',
             'previewlink': 'http://mobl-apps.com/page?cam=411&country=hu&pub=47&subid={avazu_id}&pubid={vurl}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWbaKUonKzjMIWuXeW2HmToUm3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'HU', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3149385,
             'lpname': 'Download HU', 'payout': 9.0, 'pkgname': '',
             'previewlink': 'http://mobl-apps.com/page?cam=411&country=hu&pub=47&subid={avazu_id}&pubid={vurl}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWbaKUonKzjMIWuXeU4umTerK3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'HU', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3149389,
             'lpname': 'Win IPhone7 HU', 'payout': 9.0, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWbaKUonKzjMIWuXeU4umTerm3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1,
         'traffictype': '112,105,109,102,101,113,103,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,All South Africa Carriers', 'category': '107',
         'conntype': '1,2', 'convflow': '108', 'cpnid': 2103996,
         'cpnname': 'Mobiime Mobi Mobile South Africa(One Click)',
         'description': 'No+iFraming%0D%0ANO+Clickjacking%0D%0ANo+misleading+marketing%0D%0ANo+Whatsapp+Scams',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ZA', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2276221,
             'lpname': 'Super Mario ZA (One Click)', 'payout': 4.0, 'pkgname': '',
             'previewlink': 'http://klixx.mobiime.mobi/?a=b44sDW&campID=4376&affiID=122&subid={avazu_id}',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW45eUoaKOjMIWuXeW20KW2Re3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,110,109,101,104,108'},
        {'banner': '[]', 'carrier': 'Thailand_AIS,Thailand_dtac', 'category': '107', 'conntype': '2',
         'convflow': '108', 'cpnid': 2183842, 'cpnname': 'Racing Games Thailand Mobile',
         'description': 'Campaign+Description%3A%0D%0A%0D%0AOperator+AIS+%26+DTAC+ONLY+%28one+CID+p%2F+operator%29%0D%0A%0D%0ANO+WIFI+%2C+NO+OPERA+BROWSER+%2C+NO+UC+BROWSER+%2C+NO+BROWSER+WHICH+MODIFIES+HEADER%2C+NO+IFRAMING',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'TH', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2363198,
             'lpname': 'Racing Games AIS Mobile TH', 'payout': 0.9, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW4reUJueOjMIWuXeWeHeU4amzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'TH', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2363201,
             'lpname': 'Racing Games DTAC Mobile TH', 'payout': 0.9, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW4reUJueOjMIWuXeWeHeU25e3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,110,109,101,104,108'},
        {'banner': '[]', 'carrier': 'Thailand_AIS', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2460736, 'cpnname': 'Sexy Thailand(AIS ONLY)',
         'description': 'Campaign+Description%0D%0A%0D%0AOperators+AIS+%0D%0A%0D%0ANot+allowed%3A%0D%0AIncent%0D%0AContent+Lock%0D%0ASMS+%26+Email%0D%0AVirtual+currency%0D%0AWiFi',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'TH', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2981662,
             'lpname': ' Pent House TH (AIS ONLY)', 'payout': 0.6, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWGHeN8UKOjMIWuXeWoreT9HeOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'},
            {'city': '', 'cityinclude': 2, 'country': 'TH', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2981750,
             'lpname': 'Horoscope TH (AIS ONLY)', 'payout': 0.6, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWGHeN8UKOjMIWuXeWoreT8QezjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '111,112,105,109,101,104,108'},
        {'banner': '[]', 'carrier': 'India_Reliance', 'category': '107', 'conntype': '2',
         'convflow': '108', 'cpnid': 2596504, 'cpnname': 'Bollywood India(Reliance Only)(3G Only)',
         'description': 'Mobile+targeting+%3A+IPhone+and+Android+devices+with+mobile+data+connection.+%28+2g%2C+3g%2C+4g+%29%0D%0A%0D%0ANetwork++targeting+%3A+MOBILE+DATA+CONNECTION+%28+2G%2C+3G%2C+4G+%29%0D%0A%0D%0AEXCLUSION+%3A+NO+WIFI+%2C+NO+OPERA+BROWSER+%2C+NO+UC+BROWSER+%2C+NO+BROWSER+WHICH+MODIFIES+HEADER.',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 2964356,
             'lpname': 'Bollywood IN (One Click) (Reliance Only)', 'payout': 0.3, 'pkgname': '',
             'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWjaKWj5KzjMIWuXeWoHKNeQKOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,109,101,113,104,108'},
        {'banner': '[]', 'carrier': 'WIFI,All Greece Carriers', 'category': '107', 'conntype': '1,2',
         'convflow': '101', 'cpnid': 2736382, 'cpnname': 'Play Zegmo Greece', 'description': '',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'GR', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3156757,
             'lpname': 'Google Pixel GR ', 'payout': 8.0, 'pkgname': '',
             'previewlink': 'http://play.zemgo.com/lpx/TTQyDjoNA5?aff=bck-avazu&reqid=1351231078&oid=12922&affid=60&s1=299342|',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW8UKWereOjMIWuXeU4QKW8QKRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1, 'traffictype': '112,105,110,109,101,104,108'},
        {'banner': '[]', 'carrier': 'Thailand_Truemove', 'category': '107', 'conntype': '2',
         'convflow': '108', 'cpnid': 2774717,
         'cpnname': 'Sexy Girls Thailand(One Click TrueMove Only)',
         'description': 'TARGETTING%0D%0A%0D%0AMobile+targeting+%3A+all+devices+with+mobile+data+connection.+%28+2g%2C+3g%2C+4g+%29%0D%0A%0D%0ANetwork++targeting+%3A+MOBILE+DATA+CONNECTION+%28+2G%2C+3G%2C+4G+%29%0D%0A%0D%0AEXCLUSION+%3A+NO+WIFI+%2C+NO+OPERA+BROWSER+%2C+NO+UC+BROWSER+%2C+NO+BROWSER+WHICH+MODIFIES+HEADER.',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'TH', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3243923,
             'lpname': 'Glamour Girl TH', 'payout': 0.8, 'pkgname': '', 'previewlink': '',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eW80KN8nKRjMIWuXeU2ueUoReRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1,2', 'policy': 1,
         'traffictype': '111,112,105,110,109,101,103,104,108'}, {
            'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201703\\/101\\/8b815017e5602c6e98a849fa5cf304d7.zip"]',
            'carrier': 'Poland_Plus', 'category': '101', 'conntype': '2', 'convflow': '108',
            'cpnid': 2804132, 'cpnname': 'Mobtease Poland Mobile(plus)(Adult traffic only)',
            'description': 'Restrictions%3A+Adult+Traffic+only%2C+2G%2F3G%2F4G+only+-+all+creatives+allowed+-+%28Popunders+working+very+well%29+.%0D%0A%0D%0ASpecial+Time%3A21%3A00+-+06%3A00+o%27clock+%28UTC+%2B1%29.%0D%0A%0D%0ABrowsers%3A+Apple+Webkit%2C+Chrome+Mobile%2C+Edge%2C+Opera%2C+Firefox%2C+MSIE%2C+Safari%2C+Android+Browser.%0D%0A%0D%0ACarrier%2FISP%3A+Polkomtel+Sp.+z+o.o.+%2F+Neostrada+Plus+.%0D%0A%0D%0AOne+clcik+flow.',
            'devicetype': '1,2', 'lps': [
                {'city': '', 'cityinclude': 2, 'country': 'PL', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 3359453, 'lpname': 'Plus PL (Adult traffic)', 'payout': 0.8, 'pkgname': '',
                 'previewlink': '',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ5KN4UeOjMIWuXeUeQmTGQeRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
            'minosv': '0.0', 'os': '1,2', 'policy': 1,
            'traffictype': '111,112,105,110,109,102,106,107,101,103,104,108'}, {
            'banner': '["http:\\/\\/cdn.avazu.net\\/zips\\/201703\\/114\\/223c69209e5dcc0a5fe0b575590cc8a4.zip"]',
            'carrier': 'Brazil_Claro,Brazil_Oi,Brazil_CLARO BR', 'category': '101', 'conntype': '2',
            'convflow': '108', 'cpnid': 2818201,
            'cpnname': 'Mobtease Brazil Mobile(Claro)(Adult traffic only)',
            'description': 'Restrictions%3A+Adult+Traffic+only%2C+2G%2F3G%2F4G+only+-+all+creatives+allowed.%0D%0ABrowsers%3AAndroid+Stock+Browser+%28another+Browsers+working+too%29.%0D%0A%0D%0AOS-Versions%3A+Android+4.0+-+4.4+%28another+OS-Versions+working+too%29.%0D%0A%0D%0AOne+clcik+flow.',
            'devicetype': '1,2', 'lps': [
                {'city': '', 'cityinclude': 2, 'country': 'BR', 'countryinclude': 1, 'enddate': '0000-00-00 00:00:00',
                 'enforcedv': '', 'lpid': 3359496, 'lpname': 'Claro BR (adult traffic)', 'payout': 0.3, 'pkgname': '',
                 'previewlink': '',
                 'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJnmN25e3jMIWuXeUeQmTGaKOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
            'minosv': '0.0', 'os': '1,2', 'policy': 1,
            'traffictype': '111,112,105,110,109,102,106,107,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Mexico_Telcel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2872983, 'cpnname': 'Glamour Mexico(Telcel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58c79e5412122%2F58c79e5412170.php%0D%0AGeo%3AMX%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ATelcel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'MX', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473122,
             'lpname': 'Glamour MX(Telcel)', 'payout': 3.0, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58c79e5412122/58c79e5412170.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eWoreRjMIWuXeUG0eU4ReOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Mexico_movistar', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2872984, 'cpnname': 'Glamour Mexico(Movistar) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58c79e6583df4%2F58c79e6583e44.php%0D%0AGeo%3AMX%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMovistar%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'MX', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473126,
             'lpname': 'Glamour MX(Movistar)', 'payout': 2.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58c79e6583df4/58c79e6583e44.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eWorKzjMIWuXeUG0eU4RKOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Argentina_Personal', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2872987, 'cpnname': 'Glamour Argentina(Personal) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Farg%2Findex.php%0D%0AGeo%3AAR%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3APersonal%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'AR', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473127,
             'lpname': 'Glamour AR(Personal)', 'payout': 0.7, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/arg/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eWorKRjMIWuXeUG0eU4RKRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Argentina_movistar', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2872988, 'cpnname': 'Glamour Argentina(Movistar) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Farg%2Findex.php%0D%0AGeo%3AAR%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMovistar%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'AR', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473128,
             'lpname': 'Glamour AR(Movistar)', 'payout': 0.7, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/arg/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eWormzjMIWuXeUG0eU4RmzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Indonesia_Indosat', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873044, 'cpnname': 'Glamour Indonesia(Indosat) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FindsID%2Findex.php%0D%0AGeo%3AID%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AIndosat%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ID', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473193,
             'lpname': 'Glamour ID(Indosat)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/indsID/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbuKzjMIWuXeUG0eU4aeRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Indonesia_Telkomsel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873050, 'cpnname': 'Glamour Indonesia(Telkomsel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FindsID%2Findex.php%0D%0AGeo%3AID%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ATelkomsel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ID', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473197,
             'lpname': 'Glamour ID(Telkomsel)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/indsID/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbQezjMIWuXeUG0eU4aKRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Indonesia_XL', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873054, 'cpnname': 'Glamour Indonesia(XL) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FindsID1%2Findex.php%0D%0AGeo%3AID%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AXL%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ID', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473198,
             'lpname': 'Glamour ID(XL)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/indsID1/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbQKzjMIWuXeUG0eU4amzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Sri Lanka_Airtel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873055, 'cpnname': 'Glamour Sri Lanka(Airtel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fdlg%2Findex.php%0D%0AGeo%3ALK%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AAirtel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'LK', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473200,
             'lpname': 'Glamour LK(Airtel)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/dlg/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbQK3jMIWuXeUG0eU25ezjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Sri Lanka_Dialog', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873059, 'cpnname': 'Glamour Sri Lanka(Dialog) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FLk1%2Findex.php%0D%0AGeo%3ALK%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ADialog%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'LK', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473205,
             'lpname': 'Glamour LK(Dialog)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/Lk1/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbQm3jMIWuXeUG0eU25K3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Sri Lanka_Mobitel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873063, 'cpnname': 'Glamour Sri Lanka(Mobitel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fdlg%2Findex.php%0D%0AGeo%3ALK%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMobitel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'LK', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473206,
             'lpname': 'Glamour LK(Mobitel)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/dlg/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbHeRjMIWuXeUG0eU25KOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Sri Lanka_Etisalat', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873066, 'cpnname': 'Glamour Sri Lanka(Etisalat) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FLk1%2Findex.php%0D%0AGeo%3ALK%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AEtisalat%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'LK', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473214,
             'lpname': 'Glamour LK(Etisalat)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/Lk1/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbHKOjMIWuXeUG0eU2nKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'South Africa_VodaCom', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873072, 'cpnname': 'Glamour South Africa(VodaCom) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FZAVOG%2Findex.php%0D%0AGeo%3AZA%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AVodaCom%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ZA', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473216,
             'lpname': 'Glamour ZA(VodaCom)', 'payout': 1.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/ZAVOG/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUb0eOjMIWuXeUG0eU2nKOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'United Arab Emirates_du', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873083, 'cpnname': 'Mainstream United Arab Emirates(Du) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fsub3%2Findex.php%0D%0AGeo%3AAE%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ADu%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'AE', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473228,
             'lpname': 'Mainstream AE(Du)', 'payout': 4.0, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/sub3/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbreRjMIWuXeUG0eU2RmzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'United Arab Emirates_Etisalat', 'category': '107',
         'conntype': '1,2', 'convflow': '108', 'cpnid': 2873084,
         'cpnname': 'Mainstream United Arab Emirates(Etisalat) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fetuae%2Findex.php%0D%0AGeo%3AAE%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AEtisalat%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'AE', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3473401,
             'lpname': 'Mainstream AE(Etisalat)', 'payout': 2.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/etuae/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUbrKzjMIWuXeUG0eUG5e3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Nigeria_Airtel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873371, 'cpnname': 'Glamour  Nigeria(Airtel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F107.170.173.141%2FCC%2Fafniz%2Findex.php%0D%0AGeo%3ANG%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AAirtel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'NG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476173,
             'lpname': 'Glamour NG(Airtel)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://107.170.173.141/CC/afniz/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUe0e3jMIWuXeUG0KW40eRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Nigeria_Etisalat', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873372, 'cpnname': 'Glamour Nigeria(Etisalat) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F107.170.173.141%2FCC%2Fafniz%2Findex.php%0D%0AGeo%3ANG%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AEtisalat%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'NG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476175,
             'lpname': 'Glamour NG(Etisalat)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://107.170.173.141/CC/afniz/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUe0eOjMIWuXeUG0KW40K3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Egypt_Vodafone', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873374, 'cpnname': 'Glamour Egypt(Vodafone) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fegglm%2Findex.php%0D%0AGeo%3AEG%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AVodafone%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'EG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476184,
             'lpname': 'Glamour EG(Vodafone)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/egglm/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUe0KzjMIWuXeUG0KW4rKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Egypt_Mobinil', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873375, 'cpnname': 'Glamour Egypt(Mobinil) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fegglm%2Findex.php%0D%0AGeo%3AEG%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMobinil%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'EG', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476185,
             'lpname': 'Glamour EG(Mobinil)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/egglm/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUe0K3jMIWuXeUG0KW4rK3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Colombia_Claro/Comcel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873379, 'cpnname': 'Glamour Colombia(Claro) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58bfe0e97e695%2F58bfe0e97e6e9.php%0D%0AGeo%3ACO%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AClaro%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'CO', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476189,
             'lpname': 'Glamour CO(Claro)', 'payout': 1.0, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58bfe0e97e695/58bfe0e97e6e9.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUe0m3jMIWuXeUG0KW4rm3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Colombia_movistar', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873380, 'cpnname': 'Glamour Colombia(Movistar) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58bfe1272b235%2F58bfe1272b284.php%0D%0AGeo%3ACO%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMovistar%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'CO', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476190,
             'lpname': 'Glamour CO(Movistar)', 'payout': 0.9, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58bfe1272b235/58bfe1272b284.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUerezjMIWuXeUG0KW4aezjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Colombia_Tigo', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873383, 'cpnname': 'Glamour Colombia(Tigo) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58bfe154cba0a%2F58bfe154cba5b.php%0D%0AGeo%3ACO%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ATigo%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'CO', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476192,
             'lpname': 'Glamour CO(Tigo)', 'payout': 1.0, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58bfe154cba0a/58bfe154cba5b.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUereRjMIWuXeUG0KW4aeOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Spain_Telefonica/Movistar', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873384, 'cpnname': 'Glamour Spain(Movistar) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58b53a3a7bc3a%2F58b53a3a7bca4.php%0D%0AGeo%3AES%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMovistar%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ES', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476194,
             'lpname': 'Glamour ES(Movistar)', 'payout': 0.9, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58b53a3a7bc3a/58b53a3a7bca4.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUerKzjMIWuXeUG0KW4aKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Spain_Vodafone', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873385, 'cpnname': 'Glamour Spain(Vodafone) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58b53a6ae9e43%2F58b53a6ae9e97.php%0D%0AGeo%3AES%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AVodafone%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'ES', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476201,
             'lpname': 'Glamour ES(Vodafone)', 'payout': 0.9, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58b53a6ae9e43/58b53a6ae9e97.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUerK3jMIWuXeUG0KW25e3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Russian Federation_MegaFon', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873391, 'cpnname': 'Glamour Russia(MegaFon) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58a1af9191071%2F58a1af91910c2.php%0D%0AGeo%3ARU%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMegaFon%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'RU', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476564,
             'lpname': 'Glamour RU(MegaFon)', 'payout': 0.8, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58a1af9191071/58a1af91910c2.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eUeae3jMIWuXeUG0KWjHKzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Russian Federation_Beeline', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873620, 'cpnname': 'Glamour Russia(Beeline) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58ad0e9abecbf%2F58ad0e9abed0c.php%0D%0AGeo%3ARU%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ABeeline%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'RU', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476570,
             'lpname': 'Glamour RU(Beeline)', 'payout': 0.7, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58ad0e9abecbf/58ad0e9abed0c.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9RezjMIWuXeUG0KWj0ezjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Chile_movistar', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873621, 'cpnname': 'Glamour Chile(Movistar) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58a1b02d2e9a4%2F58a1b02d2e9f8.php%0D%0AGeo%3ACL%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMovistar%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'CL', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476573,
             'lpname': 'Glamour CL(Movistar)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58a1b02d2e9a4/58a1b02d2e9f8.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9Re3jMIWuXeUG0KWj0eRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Chile_Entel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873622, 'cpnname': 'Glamour Chile(Entel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58a1b02d2e9a4%2F58a1b02d2e9f8.php%0D%0AGeo%3ACL%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AEntel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'CL', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476575,
             'lpname': 'Glamour CL(Entel)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58a1b02d2e9a4/58a1b02d2e9f8.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9ReOjMIWuXeUG0KWj0K3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Netherlands_T-Mobile', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873623, 'cpnname': 'Glamour Netherlands(T-Mobile) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FNL%2Findex.php%0D%0AGeo%3ANL%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AT-Mobile%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'NL', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476656,
             'lpname': 'Glamour NL(T-Mobile)', 'payout': 0.55, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/NL/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9ReRjMIWuXeUG0KW9QKOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Netherlands_Vodafone', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873638, 'cpnname': 'Glamour Netherlands(Vodafone) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FNL%2Findex.php%0D%0AGeo%3ANL%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AVodafone%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'NL', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476674,
             'lpname': 'Glamour NL(Vodafone)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/NL/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9UmzjMIWuXeUG0KW90KzjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Panama_Movistar', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873640, 'cpnname': 'Glamour Panama(Movistar) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58c7df4903088%2F58c7df49030db.php%0D%0AGeo%3APA%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AMovistar%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'PA', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476676,
             'lpname': 'Glamour PA(Movistar)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58c7df4903088/58c7df49030db.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9uezjMIWuXeUG0KW90KOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'Panama_Claro', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873641, 'cpnname': 'Glamour Panama(Claro) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam58c7df8362878%2F58c7df83628c6.php%0D%0AGeo%3APA%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AClaro%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'PA', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476677,
             'lpname': 'Glamour PA(Claro)', 'payout': 0.5, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam58c7df8362878/58c7df83628c6.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9ue3jMIWuXeUG0KW90KRjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'India_Aircel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873643, 'cpnname': 'Glamour India(Airtel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fmdv1g35%2Findex.php%0D%0AGeo%3AIN%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AAirtel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476679,
             'lpname': 'Glamour IN(Airtel) ', 'payout': 0.75, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/mdv1g35/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9ueRjMIWuXeUG0KW90m3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'India_Vodafone', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873644, 'cpnname': 'Glamour India(Vodafone) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fsub2%2Findex.php%0D%0AGeo%3AIN%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AVodafone%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476680,
             'lpname': 'Glamour IN(Vodafone)', 'payout': 0.65, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/sub2/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9uKzjMIWuXeUG0KW9rezjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'India_IDEA', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873645, 'cpnname': 'Glamour India(IDEA) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FAR3%2Findex.php%0D%0AGeo%3AIN%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AIDEA%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476681,
             'lpname': 'Glamour IN(IDEA)', 'payout': 0.6, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/AR3/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9uK3jMIWuXeUG0KW9re3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'India_Aircel', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873651, 'cpnname': 'Glamour India(Aircel) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2FAP%2Findex.php%0D%0AGeo%3AIN%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3AAircel%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476685,
             'lpname': 'Glamour IN(Aircel) ', 'payout': 0.45, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/AP/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9Qe3jMIWuXeUG0KW9rK3jMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'},
        {'banner': '[]', 'carrier': 'India_TATA DOCOMO', 'category': '107', 'conntype': '1,2',
         'convflow': '108', 'cpnid': 2873652, 'cpnname': 'Glamour India(TATA) Mobile',
         'description': 'Preview+link%3Ahttp%3A%2F%2F162.243.217.139%2FCC%2Fglam99%2Findex.php%0D%0AGeo%3AIN%0D%0ADaily+Cap%3AOpen%0D%0ACarrier%3ATATA%0D%0AOS%3AAndroid%0D%0AConversion+flow%3A1-click%0D%0ARestriction%3ANo+Wifi%2CNo+Pop-up%2Funder%2CRedirect+allowed',
         'devicetype': '1,2', 'lps': [
            {'city': '', 'cityinclude': 2, 'country': 'IN', 'countryinclude': 1,
             'enddate': '0000-00-00 00:00:00', 'enforcedv': '', 'lpid': 3476702,
             'lpname': 'Glamour IN(TATA)', 'payout': 0.4, 'pkgname': '',
             'previewlink': 'http://162.243.217.139/CC/glam99/index.php',
             'trackinglink': 'http://clk.apxadtracking.net/iclk/redirect.php?id=eWJ0eU9QeOjMIWuXeUG0KW85eOjMIWuXeWe5eT4-0N&trafficsourceid=23011&trackid=58cf6fc110dbe2bf'}],
         'minosv': '0.0', 'os': '1', 'policy': 1,
         'traffictype': '111,112,105,110,109,102,101,103,104,108'}], 'code': 0, 'currentpage': 1,
        'pagesize': 200, 'totalnum': 65}

    api_id = 'dsp@jetmobo.com'
    api_token = '67951dc0eec37c70b7cc33bfb9b1435d'
    yeahmobi = Yeahmobi(api_id, api_token)
    yeahmobi_result = yeahmobi.get_all_offer()
    ly = LoadYaml()
    # ly.get_login_params()
    ly.data_processing(yeahmobi_result, api_token)

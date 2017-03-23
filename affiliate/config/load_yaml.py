#!/usr/bin/env python
# encoding: utf-8

import os
import yaml
from affiliate.model.mongo_model import Provider
from affiliate.config.offer_id_list import OfferIdList
from affiliate.config.number_id_list import NumberIdList


class LoadYaml():
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # path = os.path.join(base_dir, 'config\\avazu_config.yaml')
        path = os.path.join(base_dir, 'config\yeahmobi_config.yaml')  # todo
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

        if 'offer_id' not in contents:
            print('come in offer_id_list.py')
            save_data = OfferIdList().processing_data(api_token, contents, data, loop_path, provider, save_data)
        else:
            print('come in number_id_list')
            save_data = NumberIdList().processing_data(api_token, contents, data, loop_path, provider, save_data)

        return save_data

    def list_to_dict(self, data):
        if isinstance(data, list):
            return dict(zip(range(len(data)), data))

        return data


def parse_content(self, key, data):
    content = self.y['content']
    levels = content[key]
    ret = data.get(levels, '')
    return ret

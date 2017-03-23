from jsonpath_rw import jsonpath, parse, Parent


class OfferIdList():
    """
    yeahmobi mode
    """

    def __init__(self):
        pass

    def processing_data(self, api_token, contents, data, loop_path, provider, save_data):
        loop_data = parse(loop_path).find(data)
        for loop_d in loop_data:
            tmp = {}
            tmp['provider_id'] = str(provider.id)
            tmp['api_token'] = str(api_token)
            offer_id = loop_d.path.fields[0]  # todo :try:find other way
            tmp['offer_id'] = str(offer_id)
            loop_value = loop_d.value
            # print(loop_value['payout'])
            for content in contents:
                element_keywords = contents[content]
                tmp[content] = loop_value[element_keywords]

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
        return save_data
        # for k, v in dict(parse(loop_path).find(data)[0].value).items():
        #     pass

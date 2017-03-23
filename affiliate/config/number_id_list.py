from jsonpath_rw import jsonpath, parse, Parent


class NumberIdList():
    """
    avazu mode
    """

    def __init__(self):
        pass

    def processing_data(self, api_token, contents, data, loop_path, provider, save_data):
        loop_data = parse(loop_path).find(data)
        for loop_d in loop_data:
            tmp = {}
            tmp['provider_id'] = str(provider.id)
            tmp['api_token'] = str(api_token)
            loop_value = loop_d.value
            for content in contents:
                element_keywords = contents[content]
                if '_ _ ' not in element_keywords:
                    tmp[content] = loop_value[element_keywords]

                if ('_ _ ' in element_keywords) and ('*' not in element_keywords):
                    first_parent = Parent().find(loop_d)[0].context  # todo :try:find other way like: loop_d.path.value
                    element_keywords = element_keywords[4:]
                    tmp[content] = first_parent.value[element_keywords]  # todo :error:if ont find

                if '_ _ ' in content and ' * ' in content:
                    first_parent = Parent().find(Parent().find(loop_value)[0])[0]
                    nPos = element_keywords.index('*')
                    element_keywords = element_keywords[4:nPos - 1]
                    element_parent = element_keywords
                    element_child = element_keywords[(nPos + 2):]
                    parent_lists = first_parent.value[element_parent]

                    parent_l_array = []
                    for parent_l in parent_lists:
                        parent_l_array.append(parent_l.value[element_child])

                    tmp[element_child] = parent_l_array
                    # # todo :1.th same one ;2.diff one

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

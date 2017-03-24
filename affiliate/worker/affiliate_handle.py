from affiliate.config import LoadYaml
from affiliate.rest.affiliate_request import OfferRequest
from affiliate.model.mongo_model import Provider, ApiToken, Affiliates


def affiliate(page_name=1):
    """
    affiliate auto with python
    :return:
    """
    yaml = LoadYaml()
    login_contents = yaml.get_login_params()
    provider = login_contents["provider"]
    userId = login_contents["userId"]  # todo : find it in redis
    api_url = login_contents["api_url"]
    username_keywords = login_contents["username"]
    token_keywords = login_contents['token']
    pagesize_keywords = login_contents['pagesize']
    currentpage_keywords = login_contents['currentpage']

    other_params = login_contents['other_params']

    provider = Provider.objects.get(name=provider)
    api_tokens = ApiToken.objects.filter(provider_id=str(provider.id), user_id=str(userId))

    for api_token in api_tokens:
        mode = api_token.mode  # if true:only need token,else:username&pwd
        params = {}

        if mode:
            params[token_keywords] = api_token.token
        else:
            params[username_keywords] = api_token.username
            params[token_keywords] = api_token.token

        if pagesize_keywords is not None:
            params[pagesize_keywords] = 100  # default max 100

        if currentpage_keywords is not None:
            params[currentpage_keywords] = page_name  # default first page

        if other_params is not None:
            for other_param in other_params:
                params[other_param] = other_params[other_param]

        # todo :for pages

        offers = getResult(api_url, params)
        if currentpage_keywords is not None:
            pageNumbers = yaml.getResultPages(offers)
            if pageNumbers > 0:
                for i in range(1, pageNumbers + 1):
                    params[currentpage_keywords] = i  # todo:default int (maybe str)
                    offers = getResult(api_url, params)
                    data = yaml.data_processing(offers, api_token)
                    Affiliates.save_all(data)
        else:
            data = yaml.data_processing(offers, api_token)
            Affiliates.save_all(data)


def getResult(api_url, params):
    request = OfferRequest(api_url, params=params)  # todo : header
    offers = request.get_all_offer()
    return offers

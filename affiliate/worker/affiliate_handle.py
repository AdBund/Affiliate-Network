from affiliate.config import LoadYaml
from affiliate.rest.affiliate_request import OfferRequest
from affiliate.model.mongo_model import Provider, ApiToken, Affiliates


def affiliate():
    """
    affiliate auto with python
    :return:
    """
    yaml = LoadYaml()
    login_contents = yaml.get_login_params()
    provider = login_contents["provider"]
    userId = login_contents["userId"]
    api_url = login_contents["api_url"]
    username_keywords = login_contents["username"]
    token_keywords = login_contents['token']
    pagesize_keywords = login_contents['pagesize']
    page_keywords = login_contents['page']

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
            params[pagesize_keywords] = 100  # default 100

        if page_keywords is not None:
            params[page_keywords] = 1  # default first page

        if other_params is not None:
            for other_param in other_params:
                params[other_param] = other_params[other_param]

        # todo :for pages

        request = OfferRequest(api_url, params=params)  # todo : header
        offers = request.get_all_offer()

        data = yaml.data_processing(offers, api_token)
        Affiliates.save_all(data)

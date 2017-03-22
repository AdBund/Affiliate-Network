from affiliate.config import LoadYaml
from affiliate.rest.affiliate_request import OfferRequest
from affiliate.model.mongo_model import Provider, ApiToken,Affiliates


def affiliate():
    """
    affiliate auto with python
    :return:
    """
    yaml = LoadYaml()
    login_content = yaml.get_login_params()

    provider = login_content["provider"]
    userId = login_content["userId"]
    api_url = login_content["api_url"]
    username_keywords = login_content["username"]
    token_keywords = login_content['token']
    policy_keywords = login_content['policy_k']  # approval policy of creative and landing page
    policy_value = login_content['policy_v']
    api_header = login_content['api_header']
    pagesize_keywords = login_content['pagesize']
    page_keywords = login_content['page']
    params1_k = login_content['params1_k']
    params1_v = login_content['params1_v']
    params2_k = login_content['params2_k']
    params2_v = login_content['params2_v']

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

        if policy_keywords is not None:
            params[policy_keywords] = policy_value
        if pagesize_keywords is not None:
            params[pagesize_keywords] = 100  # all api pagesize set 100
        if page_keywords is not None:
            params[page_keywords] = 1  # default first page
        if params1_k is not None:
            params[params1_k] = params1_v
        if params2_k is not None:
            params[params2_k] = params2_v

        print(params)

        # todo :for

        request = OfferRequest(api_url, params=params)  # todo : header
        offers = request.get_all_offer()

        data = yaml.data_processing(offers, api_token)
        Affiliates.save_all(data)


from affiliate.config import LoadYaml
from affiliate.model.mysql_model import AProvider, AApiToken, AAffiliates, AStatistics, db
from affiliate.rest.affiliate_request import OfferRequest


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
    token_keywords = login_content['token']  # api token keywords
    api_header = login_content['api_header']
    pagesize = login_content['pagesize']
    page = login_content['page']

    provider = AProvider.get(name=provider)
    api_tokens = (AApiToken.select(AApiToken).join(AProvider).where(AApiToken.provider_id == provider.id,
                                                                    AApiToken.userId == userId).order_by())

    for api_token in api_tokens:
        mode = api_token.mode  # if true:only need token,else:username&pwd
        params = {}

        if mode:
            params[token_keywords] = api_token.token
        else:
            params[username_keywords] = api_token.username
            params[token_keywords] = api_token.token

        params[pagesize] = 100  # all api pagesize set 100
        params[page] = 1  # default first page

        # todo :

        request = OfferRequest(api_url, params=params) # todo : header
        offers = request.get_all_offer()

        yaml.data_processing(offers,api_token)

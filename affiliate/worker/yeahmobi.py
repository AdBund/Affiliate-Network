import logging

import peewee

from affiliate.model.mysql_model import AProvider, AApiToken, AAffiliates, AStatistics, db
from affiliate.rest.yeahmobi import Yeahmobi


def yeahmobi():
    """
    yeahmobi api with python
    :return:
    """

    provider = AProvider.get(name="yeahmobi")

    # api_tokens = (AApiToken.select(AApiToken).join(AProvider).where(AProvider.id == provider.id).order_by())
    api_tokens = (AApiToken.select(AApiToken).join(AProvider).where(AApiToken.provider_id == provider.id).order_by())

    for api_token in api_tokens:
        user_name = api_token.username
        user_token = api_token.token
        # print(user_token)
        # print(user_name)

        yeahmobi = Yeahmobi(user_name, user_token)
        offers = yeahmobi.get_all_offer()  # todo : net error
        if not offers['flag'] == 'success':
            print('continue')
            continue
        offer_list = offers['data']['data']

        for offer_id in offer_list:
            offer_rows = offer_list[offer_id]
            conversion_flow = offer_rows['conversion_flow']
            exclusive = offer_rows['exclusive']
            incentive = offer_rows['incentive']
            name = offer_rows['name']
            offer_description = offer_rows['offer_description']
            offer_type = offer_rows['offer_type']
            payout = offer_rows['payout']
            preview_url = offer_rows['preview_url']
            tracklink = offer_rows['tracklink']

            # todo:
            # offer_s = list(map(lambda offer_rows: {
            #     'conversion_flow': offer_rows['conversion_flow']
            # }, offer_list[offer]))



            # save in mysql

            doc = {
                'provider': provider,
                'api_token': api_token,
                'affiliate_identity': offer_id,
                'name': name,
            }

            try:
                AAffiliates.insert(doc).execute()
            except peewee.IntegrityError:
                logging.warning('data already exists')
                pass
            except Exception as e:
                logging.warning(e)
                pass

            statistics = {
                'provider': provider,
                'api_token': api_token,
                'affiliate': AAffiliates.get(provider=provider, affiliate_identity=offer_id),
                #
                'conversion_flow': conversion_flow,
                'exclusive': exclusive,
                'incentive': incentive,
                # 'name': name,
                'offer_description': offer_description,
                'offer_type': offer_type,
                'payout': payout,
                'preview_url': preview_url,
                'tracklink': tracklink,
            }

            try:
                AStatistics.insert(statistics).execute()
            except peewee.IntegrityError:
                logging.warning('data already exists')
                pass
            except Exception as e:
                logging.warning(e)
                pass

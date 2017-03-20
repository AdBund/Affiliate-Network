import datetime
import json
import logging
import traceback

import peewee

from affiliate.model.mysql_model import AProvider, AApiToken, AAffiliates, AStatistics, db
from affiliate.rest.avazu import Avazu
from affiliate.model.mongo_model import MGAAffiliates
import time


def avazu():
    """
    yeahmobi api with python
    :return:
    """

    provider = AProvider.get(name="avazu")
    api_tokens = (AApiToken.select(AApiToken).join(AProvider).where(AApiToken.provider_id == provider.id).order_by())

    for api_token in api_tokens:
        user_name = api_token.username
        user_token = api_token.token

        avazu = Avazu(user_name, user_token)
        offers = avazu.get_all_offer()  # todo : net error
        if offers['code'] == 1:
            print('continue')
            continue
        offer_list = offers['campaigns']

        for offer in offer_list:
            conversion_flow = offer['convflow']
            offer_id = offer['cpnid']
            # exclusive = offer_id['exclusive']
            # incentive = offer_id['incentive']
            name = offer['cpnname']
            offer_description = offer['description']
            offer_type = offer['traffictype']

            carriers = offer['carrier']
            category = offer['category']
            country = ''
            payout = ''
            preview_url = ''
            tracklink = ''

            lps = offer['lps']

            # save in mysql

            doc = {
                'provider': provider,
                'api_token': api_token,
                'affiliate_identity': offer_id,
                'name': name,
            }

            try:
                MGAAffiliates.objects(provider_id=provider.id, offer_id=offer_id).delete()
                MGAAffiliates(provider_id=provider.id,
                              offer_id=offer_id,
                              date=datetime.datetime.now(),
                              raw=offer).save()
                AAffiliates.insert(doc).execute()

            except peewee.IntegrityError:
                logging.warning(' doc data already exists')
                pass
            except Exception as e:
                logging.warning(e)
                pass

            for lp in lps:
                country = lp['country']
                payout = lp['payout']
                preview_url = lp['previewlink']
                tracklink = lp['trackinglink']

                statistics = {
                    'carriers': carriers,
                    'countries': country,
                    'category': category,
                    'provider': provider,
                    'api_token': api_token,
                    'affiliate': AAffiliates.get(provider=provider, affiliate_identity=offer_id),
                    'conversion_flow': conversion_flow,
                    'offer_description': offer_description,
                    'offer_type': offer_type,
                    'payout': payout,
                    'preview_url': preview_url,
                    'tracklink': tracklink,
                    # 'date': datetime.datetime.now(),
                }

                print('-----------------------')
                try:
                    AStatistics.insert(statistics).execute()
                except peewee.IntegrityError:
                    logging.warning(' statistics data already exists')
                    pass
                except Exception as e:
                    traceback.print_exc()
                    logging.warning(e)
                    pass

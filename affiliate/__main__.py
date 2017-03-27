import json

from affiliate.worker import affiliate_handle
from affiliate.model.redis_model import R
from affiliate.model.mongo_model import Provider

if __name__ == '__main__':
    # r = R()
    # while True:
    # queue = json.loads(r.rpop('queue'))  # {uuid:{'provider_id':123,'user_id':123}}
    # data = {'uuid': {'provider_id': 123, 'user_id': 123}}
    # uuid = list(data.keys())[0]
    # provider_id, user_id = list(list(data.values())[0].keys())[0], list(list(data.values())[0].values())[0]
    affiliate_handle.affiliate(file_name=Provider.get_by_id('58d8825b1dc8e127166ad97c').name,
                               userId=71)

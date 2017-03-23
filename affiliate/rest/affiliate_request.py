import requests


class OfferRequest(object):
    def __init__(self, url, params):
        self.url = url
        self.params = params

    def get_all_offer(self, method="GET"):
        url = self.url
        params = self.params
        response = requests.request(method, url=url, params=params)
        print(response.text)
        # return response.json()

    def offer_operate(self):
        pass  # todo



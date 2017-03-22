import requests


class Yeahmobi():
    def __init__(self, api_username, api_token):
        self.api_id = api_username
        self.api_token = api_token

    def get_all_offer(self):
        url = 'http://sync.yeahmobi.com/sync/offer/get'
        header = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        query = {
            'api_id': self.api_id,
            'api_token': self.api_token,
            'limit': 100,
            'page': 1,
        }
        response = requests.request("GET", url, params=query)
        # return response.text
        return response.json()


if __name__ == '__main__':
    api_id = 'dsp@jetmobo.com'
    api_password = 'Ihave2cars$'
    api_token = '67951dc0eec37c70b7cc33bfb9b1435d'
    yeahmobi = Yeahmobi(api_id, api_token)
    print(yeahmobi.get_all_offer())
    # todo: token is password for md5, note!

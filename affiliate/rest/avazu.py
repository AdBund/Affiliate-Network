import requests


class Avazu():
    def __init__(self, api_username, api_token):
        self.api_id = api_username
        self.api_token = api_token

    def get_all_offer(self):
        url = 'http://api.c.avazutracking.net/performance/v2/getcampaigns.php'
        header = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        query = {
            'uid': self.api_id,
            # 'page': 1,
            'sourceid': self.api_token,
        }
        response = requests.request("GET", url, params=query)
        # return response.text
        return response.json()


if __name__ == '__main__':
    api_id = '18629'
    api_token = '23011'  # dsp
    # api_token = '22433'# incentive traffic
    # api_token = '22417'# FB
    # api_token = '22416'# Google Adwords
    avazu = Avazu(api_id, api_token)
    print(avazu.get_all_offer())

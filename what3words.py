import requests
import json


def get3words(lat, lng):
    return json.loads(
        requests.get('https://api.what3words.com/position?key=9GYM2AK4&position=' +
                     ','.join([str(lat), str(lng)])).text)['words']

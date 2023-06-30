from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import os
import requests
import urllib.parse

url = f'https://cryptopanic.com/api/v1/posts/?auth_token=fbcd3473b63c589bd20c681ff435593f6f33c6fa&kind=news'

session = Session()
try:
    response = session.get(url)
    data = json.loads(response.text)
    titles={}
    for i in range(20):
        titles[data['results'][i]['title']] =  data['results'][i]['url']
    for title in titles:
        print(titles[title])
except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)    
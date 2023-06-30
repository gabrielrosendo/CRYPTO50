import os
import requests
import urllib.parse

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def lookup(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': symbol,
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'bfa5d5f6-074f-492e-9abf-cb411f4a0ba4',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return {
            "name": data['data'][symbol]['name'],
            "price": data['data'][symbol]['quote']['USD']['price'],
            "change_24": data['data'][symbol]['quote']['USD']['percent_change_24h'],
            "change_7": data['data'][symbol]['quote']['USD']['percent_change_7d']
        }
    except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            
def usd(value):
    return f"${value:,.2f}"


def check():
    url = f'https://cryptopanic.com/api/v1/posts/?auth_token=fbcd3473b63c589bd20c681ff435593f6f33c6fa&kind=news'

    session = Session()
    try:
       response = session.get(url)
       data = json.loads(response.text)
       titles={}
       for i in range(15):
           titles[data['results'][i]['title']] =  data['results'][i]['url']
       return(titles)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)    
    
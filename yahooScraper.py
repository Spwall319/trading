import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', class_  = class_path)
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts
def real_time_prices(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '/'

    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.content, 'html.parser')
        texts = web_content_div(web_content, "container yf-aay0dk")
        if texts != []:
            day = {}
            day['price'] = texts[0]
            day['change'] = texts[1]
            day['perChange'] = texts[2][1:-1]
            if len(texts) > 4:
                after = {}
                after['price'] = texts[4]
                after['change'] = texts[5]
                after['perChange'] = texts[6][1:-1]
                return day, after
        else:
            day = {}
    except ConnectionError:
        day = {}
    return day, {}

Stock = ['NVDA', 'TIGR', 'MTTR']
for s in Stock:
    print("Ticker: " + s)
    lst = real_time_prices(s)
    for key, val in lst[0].items():
        print(key + ": " + val)
    if lst[1]:
        print('\nAfter Hours:')
        for key, val in lst[1].items():
            print(key + ": " + val)
    print('\n')

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

def get_stock_info(web_content, class_path):
    info = {}
    web_content_div = web_content.find_all('div', attrs = {'class':class_path, 'data-testid':'quote-statistics'})
    try:
        lis = web_content_div[0].find_all('li')
        for li in lis:
            spans = li.find_all('span')
            info[spans[0].get_text()] = spans[1].get_text()
    except IndexError:
        info = {}
    return info

def real_time_prices(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code + '/'

    info = {}
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
            else:
                after = {}
        else:
            day = {}
            after = {}

        info = get_stock_info(web_content, 'container yf-tx3nkj')
    except ConnectionError:
        day = {}
        after = {}
        info = {}
    return day, after, info

Stock = ['NVDA', 'TIGR', 'MTTR']

while (True):
    info = []
    for s in Stock:
        time_stamp = datetime.datetime.now()
        time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
        lst = real_time_prices(s)
        day = lst[0]
        after = lst[1]
        inf = lst[2]
        if not after:
            info.append(s)
            info.extend([day['price']])
            info.extend([day['change']])
            info.extend([day['perChange']])
        else:
            info.append(s)
            info.extend([after['price']])
            info.extend([after['change']])
            info.extend([after['perChange']])
        info.extend([inf['Volume']])
        info.extend([inf['1y Target Est']])
        col = [time_stamp]
        col.extend(info)
        df = pd.DataFrame(col)
        df = df.T
    df.to_csv(str(time_stamp[0:11] + 'stock data.csv'), mode='a', header=False)

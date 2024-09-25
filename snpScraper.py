import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from yahooScraper import *

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('tr',  class_ = class_path)
    texts = []
    for cont in web_content_div:
        if cont:
            tds = cont.find_all('td')
            text = [td.get_text() for td in tds]
            if text:
                texts.append(text)
    return texts

url = 'https://stockanalysis.com/list/sp-500-stocks/'
r = requests.get(url)
web_content = BeautifulSoup(r.content, 'html.parser')
texts = web_content_div(web_content, "svelte-eurwtr")
stocks = {}
for txt in texts:
    stocks[int(txt[0])] = {'Symbol': txt[1], 'Name': txt[2], 'Market Cap': txt[3], 'Price': txt[4], '% Change': txt[5], 'Revenue': txt[6]}


s = stocks[5]
print("Ticker: " + s['Name'])
lst = real_time_prices(s['Symbol'])
for key, val in lst[0].items():
    print(key + ": " + val)
if lst[1]:
    print('\nAfter Hours:')
    for key, val in lst[1].items():
        print(key + ": " + val)
print('\n')


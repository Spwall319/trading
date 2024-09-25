import requests
from bs4 import BeautifulSoup

def all_symbols(web_content, class_path):
    web_content_div = web_content.find_all('tr',  class_ = class_path)
    companies = {}
    symbols = {}
    industry = {}
    marketCap = {}
    first = True
    for cont in web_content_div:
        print(cont)
        if first:
            first = False
            continue
        if cont:
            tds = cont.find_all('td')
            text = [td.get_text() for td in tds]
            symbols[text[0]] = {'Symbol': text[0], 'Name': text[1], 'Industry': text[2], "Market Cap": text[3]}
            companies[text[1]] = {'Symbol': text[0], 'Name': text[1], 'Industry': text[2], "Market Cap": text[3]}
            industry[text[2]] = {'Symbol': text[0], 'Name': text[1], 'Industry': text[2], "Market Cap": text[3]}
            marketCap[text[3]] = {'Symbol': text[0], 'Name': text[1], 'Industry': text[2], "Market Cap": text[3]}
    return companies, symbols, industry, marketCap

def get_symbol(web_content, class_path, name):
    web_content_div = web_content.find_all('tr', class_=class_path)
    first = True
    for cont in web_content_div:
        print(cont)
        if first:
            first = False
            continue
        if cont:
            tds = cont.find_all('td')
            text = [td.get_text() for td in tds]
            if text[1] == name:
                return text[0]


url = 'https://stockanalysis.com/stocks/'
r = requests.get(url)
web_content = BeautifulSoup(r.content, 'html.parser')
companies, symbols, industry, marketCap = all_symbols(web_content, "svelte-eurwtr")

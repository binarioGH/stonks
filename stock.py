#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup



def format_date(date_datetime):
    date_timetuple = date_datetime.timetuple()
    date_mktime = time.mktime(date_timetuple)
    date_int = int(date_mktime)
    date_str = str(date_int)
    return date_str


def subdomain(
    symbol,
    start,
    end,
    filter='history',
    ):
    subdoma = '/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter={3}&frequency=1d'
    subdomain = subdoma.format(symbol, start, end, filter)
    return subdomain


def header_function(subdomain):
    hdrs = {
        'authority': 'finance.yahoo.com',
        'method': 'GET',
        'path': subdomain,
        'scheme': 'https',
        'accept': 'text/html',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64)',
        }

    return hdrs


def scrape_page(url, header):
    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.text, "html.parser")
    rows = soup.find_all("tr")[1:]
    chart_data = {}
    for row in rows:
        entries = row.find_all("td")
        try:
            date = entries[0].text
            price = float(entries[1].text)
            chart_data[date] = price
        except:
            pass

    return chart_data


def get_history(symbol, days=365):

    dt_start = datetime.today() - timedelta(days=days)
    dt_end = datetime.today()

    start = format_date(dt_start)
    end = format_date(dt_end)

    sub = subdomain(symbol, start, end)
    header = header_function(sub)

    base_url = 'https://finance.yahoo.com'
    url = base_url + sub
    price_history = scrape_page(url, header)
    return price_history

def get_current_value(symbol):
    content = requests.get("https://finance.yahoo.com/quote/{}".format(symbol), headers=header_function("/quote/{}".format(symbol)))
    soup = BeautifulSoup(content.text, "html.parser")
    price = float(soup.find_all("span", {"Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})[0].text)
    return price

def get_name(symbol):
    try:
        content = requests.get("https://finance.yahoo.com/quote/{}".format(symbol), headers=header_function("/quote/{}".format(symbol)))
        soup = BeautifulSoup(content.text, "html.parser")
        title = soup.find_all("h1", {"class": "D(ib) Fz(18px)"})[0].text.split(".")[0]
    except:
        return "Couldn't find the name!"
    return title


def get_hot_stocks(): #Go to cnn to check what are the most important stocks
    hot_stocks = {} #Crete dictionary to store the stocks
    content = requests.get("https://money.cnn.com/data/hotstocks/")
    soup = BeautifulSoup(content.text, "html.parser")

    rows = soup.find_all("tr")
    for row in rows:
        if "Company" in row.text:
            continue
        bigboi = BeautifulSoup(str(row), "html.parser")

        symbol = bigboi.find_all("a", {"class": "wsod_symbol"})[0].text
        if symbol in hot_stocks:
            continue

        hot_stocks[symbol] = {"company": "", "price": 0.0, "change": "%"}

        columns = bigboi.find_all("td")

        hot_stocks[symbol]["company"] = columns[0].span.text
        hot_stocks[symbol]["price"] = columns[1].span.text
        hot_stocks[symbol]["change"] = columns[-1].span.text

    return hot_stocks


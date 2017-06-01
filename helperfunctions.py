# Installation instructions:
# pip install quandl
# 
# # Quandl key: 1KpUKQyWwNyxFK1Er6pq
import quandl
import json


with open('tickers.json') as data_file:
    tickers = json.load(data_file)

quandl.ApiConfig.api_key = "1KpUKQyWwNyxFK1Er6pq"

def get_quote(ticker):
    ticker = ticker.upper()
    stock_name = None
    for stock in tickers:
        if stock["Ticker"] == ticker:
            stock_name = stock["Name"] 
    if (stock_name == None):
        return None
    # Retrieve the most recent stock quote data in the table
    data = quandl.get_table('WIKI/PRICES', ticker=ticker, qopts={'columns': ['close']}, date = { 'gt': '2017-05-20'})
    # print(len(data))
    if (len(data) == 0):
        return None
    print(data["close"][len(data) - 1])
    stock_quote = {}
    stock_quote["ticker"] = ticker
    stock_quote["name"] = stock_name
    stock_quote["price"] = data["close"][len(data) - 1]
    return stock_quote


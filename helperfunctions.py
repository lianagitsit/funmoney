# Installation instructions:
# pip install quandl
# 
# # Quandl key: 1KpUKQyWwNyxFK1Er6pq
import quandl
import json

quandl.ApiConfig.api_key = "1KpUKQyWwNyxFK1Er6pq"


with open('spfive.json') as data_file:
    big_stock_list = json.load(data_file)

# Delete any rows for stocks that aren't in the quandl database
# This is an embarassing hack please don't tell my mother

# for stock in big_stock_list:
#    data = quandl.get_table('WIKI/PRICES', ticker=stock["Ticker"], qopts={'columns': ['close']}, date = { 'gt': '2017-06-14'})
#     if (len(data) == 0):
#        big_stock_list.remove(stock)

# end hack




def get_quote(ticker):
    ticker = ticker.upper()
    stock_name = None
    for stock in big_stock_list:
        if stock["Symbol"] == ticker:
            stock_name = stock["Name"] 
    if (stock_name == None):
        return None
    # Retrieve the most recent stock quote data in the table
    data = quandl.get_table('WIKI/PRICES', ticker=ticker, qopts={'columns': ['close']}, date = { 'gt': '2017-06-14'})
    # print(len(data))
    if (len(data) == 0):
        return None
    # print(data["close"][len(data) - 1])
    stock_quote = {}
    stock_quote["ticker"] = ticker
    stock_quote["name"] = stock_name
    stock_quote["price"] = data["close"][len(data) - 1]
    return stock_quote

def get_stock_list():
    return big_stock_list


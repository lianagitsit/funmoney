# Installation instructions:
# pip install quandl
# 
# # Quandl key: 1KpUKQyWwNyxFK1Er6pq
import quandl
import json
# import time
import datetime

quandl.ApiConfig.api_key = "1KpUKQyWwNyxFK1Er6pq"

# Load the S&P500 stock list into a list of dictionaries
with open('spfive.json') as data_file:
    big_stock_list = json.load(data_file)

# Prepare a list of cached stock quotes
cached_quotes = []

today = datetime.datetime.now()
print("Today is " + str(today))




def get_quote(ticker):
    ticker = ticker.upper()
    # See if a cached quote exists
    for quote in cached_quotes:
        if (quote["ticker"] == ticker):
            # if it exists, see how old it is 
            time_elapsed = datetime.datetime.now() - quote["timestamp"]
            print("|#@# debug #@#|>>> The quote exists! It is " + str(time_elapsed.total_seconds()) + " seconds old <<<")
            # If it's less than 30 minutes old, use cached version
            if (time_elapsed.total_seconds() < 1800):
                print ("|#@# debug #@#|>>> You have a cached quote, and so I am returning it <<<")
                return quote
            # Otherwise, remove the old cached value and continue
            print("|#@# debug #@#|>>> You have a stale quote, so I am removing it <<<")
            cached_quotes.remove(quote)

    # prepare dummy data to return if there's an error with quandl
    error_quote = {}
    error_quote["ticker"] = "ERROR!"
    error_quote["name"] = "Ticker Not Found"
    error_quote["price"] = 0
    error_quote["timestamp"] = datetime.datetime.now()
    # Try to find and return a quote
    
    stock_name = None
    for stock in big_stock_list:
        if stock["Symbol"] == ticker:
            stock_name = stock["Name"] 
    if (stock_name == None):
        return error_quote
    # Retrieve the most recent stock quote data in the table
    data = quandl.get_table('WIKI/PRICES', ticker=ticker, qopts={'columns': ['close']}, date = { 'gt': '2017-06-14'})
    # If no useable data returned, return the error quote
    if (len(data) == 0):
        return error_quote
    # Build the stock quote, save it to the cache, and return it
    stock_quote = {}
    stock_quote["ticker"] = ticker
    stock_quote["name"] = stock_name
    stock_quote["price"] = data["close"][len(data) - 1]
    stock_quote["timestamp"] = datetime.datetime.now()
    cached_quotes.append(stock_quote)
    print("|#@# debug #@#|>>> New quote retrieved from quandl and returned <<<")
    print("|#@# debug #@#|>>> Current cached quotes: ")
    for quote in cached_quotes:
        print("|#@# debug #@#|>>> Ticker: " + quote["ticker"] + "... ")
    return stock_quote

def get_stock_list():
    return big_stock_list


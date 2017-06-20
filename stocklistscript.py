import quandl
import json

quandl.ApiConfig.api_key = "1KpUKQyWwNyxFK1Er6pq"


with open('fewertickers.json') as data_file:
    big_stock_list = json.load(data_file)

begin_stocks = str(len(big_stock_list))
print("Your file began with " + begin_stocks + " stocks in it!")


# Delete any rows for stocks that aren't in the quandl database
# This is an embarassing hack please don't tell my mother

safety_valve = 0

for stock in big_stock_list:
    safety_valve += 1
    print("Testing " + stock["Ticker"])
    data = quandl.get_table('WIKI/PRICES', ticker=stock["Ticker"], qopts={'columns': ['close']}, date = { 'gt': '2017-06-14'})
    if (len(data) == 0):
        print("Removed " + stock["Ticker"])
        big_stock_list.remove(stock)
    if (safety_valve > 600):
        print ("Ok that's plenty for now!")
        break        

with open('fewertickers.json', 'w') as outfile:
    json.dump(big_stock_list, outfile)

print ("You started with " + begin_stocks + " stocks, and now have " + str(len(big_stock_list)) + " stocks after this run!")

# end hack
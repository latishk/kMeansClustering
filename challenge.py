__author__ = 'harshal'
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import datetime
from bs4 import BeautifulSoup
import pandas as pd
from pandas import Series, DataFrame
import numpy

START_DATE = datetime.date(2015, 1, 1)
YESTERDAY =  datetime.date.today() - datetime.timedelta(days=1)

#print(END_DATE)

def get_tickers():
    
    request_page = urllib2.Request('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    open = urllib2.urlopen(request_page)
    markup = open.read().decode()
    soup = BeautifulSoup(markup, "html.parser")
    tables = soup.find_all('table')
    external_class = tables[0].findAll('a', {'class':'external text'})
    tickers = []
    for ext in external_class:
        if not 'reports' in ext:
            tickers.append(ext.string)
    print(tickers)
    return tickers

def get_dataframe(ticker_symbol, start_date, end_date):
    return pd.io.data.get_data_yahoo(ticker_symbol,start_date, end_date)                         

def compute_highest_deviation():
     data_dictionary = {}
     max_deviation_ticker=""
     max = -1
     for ticker in get_tickers():
         data_frame = get_dataframe(ticker, START_DATE, YESTERDAY)
         adj_close = data_frame['Adj Close']
         data_dictionary[ticker] = data_frame
         
         std_dev = numpy.std(adj_close)
         if max <= std_dev:
             max = std_dev
             max_deviation_ticker = ticker
             print(max_deviation_ticker)
    
     return max_deviation_ticker
         
print("the stock with highest deviation is: ",compute_highest_deviation())
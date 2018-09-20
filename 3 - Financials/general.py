import sqlite3
import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import numpy as np
import time
from random import randint


# SQL 
conn = sqlite3.connect('Stock_list.sqlite')
cur = conn.cursor()
cur.execute('''PRAGMA journal_mode = OFF''')
cur.execute('DROP TABLE IF EXISTS general')

# TICKER STOCK
ticker_list = ['aveo','irbt']

# PICK TICKER SYMBOLS
file_name = 'biotech_tickers.csv'

tickerdf = pd.read_csv(file_name)

ticker_list = tickerdf['TICKER'].tolist()

def market_cap_f (ticker):

	# PICK INCOME, BALANCE SHEET, OR CASHFLOW

	url = 'https://www.nasdaq.com/symbol/' + ticker
		
	# OPEN URL

	html = urllib.request.urlopen(url).read()

	html = html.decode()

	table = html.split('Market Cap')
    
	company_market_cap = re.findall('([0-9]+,[0-9]+,?[0-9]+,?[0-9]+)',table[1])
	
	company_market_cap = [w.replace(',', '') for w in company_market_cap]
			
	company_market_cap = list(map(int, company_market_cap))

	return (company_market_cap[0])

def pe_ratio_f (ticker):

	# PICK INCOME, BALANCE SHEET, OR CASHFLOW

	url = 'https://www.nasdaq.com/symbol/' + ticker
		
	# OPEN URL

	html = urllib.request.urlopen(url).read()

	html = html.decode()

	table = html.split('P/E Ratio:')
    	
	pe_ratio = re.findall('([0-9]+)',table[1])
	
	pe_ratio = [w.replace(',', '') for w in pe_ratio]
			
	pe_ratio = list(map(int, pe_ratio))

	return (pe_ratio[0])

# DATAFRAME
finaldf = pd.DataFrame(columns = [])
	
for ticker in ticker_list :

	try:
		# RANDOM TIME
		rand_time = randint(60, 90)
		
		print (rand_time)
		
		# SLEEP
		time.sleep(rand_time)

		# CREATE DATABASE
		data_line = {'Market_Cap': market_cap_f(ticker),
					'PE-Ratio': pe_ratio_f(ticker)
					}
		
		newdf = pd.DataFrame(data = data_line,index = [ticker])
		finaldf = pd.concat([finaldf,newdf], axis = 0)
		
		print (finaldf)
		
	except:
		continue
	
print (finaldf)
	
finaldf.to_sql('general',conn,if_exists = 'append')

	
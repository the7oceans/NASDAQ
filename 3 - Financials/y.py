import sqlite3
import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import numpy as np
import time
from random import randint
from selenium import webdriver


# SQL 
conn = sqlite3.connect('Stock_list.sqlite')
cur = conn.cursor()
cur.execute('''PRAGMA journal_mode = OFF''')
cur.execute('DROP TABLE IF EXISTS general')

# TICKER STOCK
ticker_list = ['aveo']

'''
# PICK TICKER SYMBOLS
file_name = 'biotech_tickers.csv'

tickerdf = pd.read_csv(file_name)

ticker_list = tickerdf['TICKER'].tolist()
'''
# MINER


finaldf = pd.DataFrame(columns = [])
	
for ticker in ticker_list :	

	url = 'view-source:https://www.benzinga.com/stock/' + ticker
	
	html = urllib.request.urlopen(url).read()

	html = html.decode()
		

	




	
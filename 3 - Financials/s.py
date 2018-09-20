import sqlite3
import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# GET SQL
# CREATE DATABASE TO STORE DATA
conn = sqlite3.connect('Stock_list.sqlite')
cur = conn.cursor()
cur.execute('''PRAGMA journal_mode = OFF''')
cur.execute('DROP TABLE IF EXISTS finance')


# GET TABLE FUNCTION
def get_table_info(html,ticker,f_type):

	# SPLIT THE HTML CODE
	table = html.split('<th bgcolor="#e6e6e6">')

	table = table[1:]
	
	print (len(table))
	
	#---------------------------------------------
	# PULL FINANCIALS INFORMATION

	# SET UP
	statementdf = pd.DataFrame(columns=[])
		
	count = -1

	name_count = 0

	for line in table:
		
		name_count = name_count + 1
		
		count = count + 1
		
		# GET COLUMN HEADERS
		table_name = re.findall('(.+?)</th>',line)
		
		# PULLS QUARTER INFO
		
		quarter = re.findall('<td>(.+?)<',line)
		
		# FILTERS FOR $ VALUE
		quarter = filter(lambda k: '$' in k, quarter)
		
		# REPLACES , with NULL			
		quarter = [w.replace(',', '') for w in quarter]
		
		# REPLACES $ WITH NULL
		quarter = [w.replace('$', '') for w in quarter]
		
		# REPLACE NEGATIVE
		quarter = [w.replace('(', '-') for w in quarter]
		
		quarter = [w.replace(')', '') for w in quarter]
		
		# NAMES EACH ROW A UNIQUE VALUE
		table_row_name = str(name_count) + ' - ' + table_name[0]
		
		Q1 = 'Q1_' + ticker.upper()
		Q2 = 'Q2_' + ticker.upper()
		Q3 = 'Q3_' + ticker.upper()
		Q4 = 'Q4_' + ticker.upper()
		
		# CREATE STAMENTS			
		data_row = {'Year_2017':table_row_name,
					'Type': f_type,
					 Q1 : float(quarter[0]),
					 Q2 : float(quarter[1]),
					 Q3: float(quarter[2]),
					 Q4: float(quarter[3])
				   }
		
		newdf = pd.DataFrame(data=data_row, index = [count])
		
		statementdf = pd.concat([statementdf,newdf],axis = 0)
		
	return (statementdf)

# SELENIUM 
driver = webdriver.Edge()

# PULL WEBSITE
driver.get('https://www.nasdaq.com')


# STOCK
'''
ticker_list = ['aveo','hub','irbt']
'''

# PICK TICKER SYMBOLS
file_name = 'biotech_tickers.csv'

tickerdf = pd.read_csv(file_name)

ticker_list = tickerdf['TICKER'].tolist()

# SETUP
finaldf = pd.DataFrame(columns=[])

for ticker in ticker_list:

	try:

		# GET STOCK 
		elem = driver.find_element_by_id('stock-search-text')
		elem.send_keys(ticker)
		elem.send_keys(Keys.RETURN)
		
		print (ticker)

		time.sleep(10)

		# GET INCOME STATEMENT
		income = driver.find_element_by_id('fulllink')
		income.click()

		time.sleep(10)

		html = driver.page_source

		income_df = get_table_info(html,ticker,'income')

		# BALANCE SHEET
		balance = driver.find_element_by_xpath('//*[@id="tab2"]/span')
		balance.click()

		time.sleep(10)

		html = driver.page_source

		balance_df = get_table_info(html,ticker,'balance')

		# CASHFLOW
		cashflow = driver.find_element_by_xpath('//*[@id="tab3"]/span')
		cashflow.click()

		time.sleep(10)

		html = driver.page_source

		cashflow_df = get_table_info(html,ticker,'cashflow')

		# MERGE 
		company_df = pd.concat([income_df,balance_df,cashflow_df],axis = 0)

		# MERGE TO MASTER LIST
		finaldf = pd.concat([finaldf,company_df],axis = 1)
		
	except:
		continue

		
# REMOVE DUPICATES
finaldf = finaldf.T.drop_duplicates().T

# CH
finaldf = finaldf.set_index('Year_2017')

# SEND TO CSV
finaldf.to_csv('Statement.csv')

# SEND TO SQL
finaldf.to_sql('finance',conn,if_exists = 'append')

driver.close()






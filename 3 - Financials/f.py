import sqlite3
import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import numpy as np
import time

# SHOW ALL ROWS
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

# CREATE DATABASE TO STORE DATA
conn = sqlite3.connect('Stock_list.sqlite')
cur = conn.cursor()
cur.execute('''PRAGMA journal_mode = OFF''')
cur.execute('DROP TABLE IF EXISTS finance')

'''
# PICK TICKER SYMBOLS
file_name = 'biotech_tickers.csv'

tickerdf = pd.read_csv(file_name)

ticker_list = tickerdf['TICKER'].tolist()
'''

# STOCK
ticker_list = ['aveo','irbt']

# SET UP
finaldf = pd.DataFrame(columns=[])

# GET FINANCIAL INFORMATION
for ticker in ticker_list :

	try:

		print ('\n',ticker,'COMPANY STATEMENT----------------')
		
		ticker = ticker.lower()

		name_count = 0
		
		companydf = pd.DataFrame(columns=[])

		# PICK INCOME, BALANCE SHEET, OR CASHFLOW

		url = 'https://www.nasdaq.com/symbol/' + ticker
		
		url_income = url + '/financials?query=income-statement'
		
		url_balance = url + '/financials?query=balance-sheet'
	   
		url_cashflow = url + '/financials?query=cash-flow'
		
		url_list = [url_income,url_balance,url_cashflow]
			
		for url in url_list :
			
			print (url)
						
			# PRINT URL
			html =	urllib.request.urlopen(url).read()
			
			html = html.decode()

			# SPLIT THE DATA INTO LINES
			table = html.split('<th bgcolor="#E6E6E6">')

			table = table[1:]

			#---------------------------------------------
			# PULL FINANCIALS INFORMATION

			# SET UP
			statementdf = pd.DataFrame(columns=[])
				
			count = -1

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
				
				# NAMES EACH ROW A UNIQUE VALUE
				table_row_name = str(name_count) + ' - ' + table_name[0]
				
				Q1 = 'Q1_' + ticker.upper()
				Q2 = 'Q2_' + ticker.upper()
				Q3 = 'Q3_' + ticker.upper()
				Q4 = 'Q4_' + ticker.upper()
				
				# CREATE STAMENTS			
				data_row = {'Year_2017':table_row_name,
							 Q1 : quarter[0],
							 Q2 : quarter[1],
							 Q3: quarter[2],
							 Q4: quarter[3]
						   }
				
				newdf = pd.DataFrame(data=data_row, index = [count])
				
				statementdf = pd.concat([statementdf,newdf],axis = 0)
		
			# PULL TOGETHER STATEMENTS
			companydf = pd.concat([companydf,statementdf],axis = 0)
			
		# MERGE COMPANY TOGETHER
		finaldf = pd.concat([finaldf,companydf],axis = 1)

	except:
		continue

finaldf = finaldf.astype('str')

# REMOVE DUPLICATE COLUMNS & SET INDEX

finaldf = finaldf.T.drop_duplicates().T

finaldf = finaldf.set_index('Year_2017')

# SEND TO CSV
finaldf.to_csv('Statement.csv')

# SEND TO SQL
finaldf.to_sql('finance',conn,if_exists = 'append')

#2601:182:c77f:e7b2:90d7:70a1:e231:f4d0



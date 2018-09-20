import sqlite3
import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import numpy as np
import os
import sys

# IMPORT FUNCTIONS 
user_name = os.getenv("USERNAME")
path_finder = r'C:\\Users\\' + user_name + '\\Google Drive\\2 - Code'
sys.path.append(path_finder)

# IMPORT DRUG DATABASE
url = 'https://www.biopharmcatalyst.com/biotech-stocks/company-pipeline-database'

html = urllib.request.urlopen(url).read()

html = html.decode()

# SPLICE DRUGS
html = html.split('<tr class="js-drug js-td--fda"')

html = html[1:]

# SET UP MINER
finaldf = pd.DataFrame(columns = [])

count = 0

for line in html:

	# COMPANY TICKER TRANSFORM
	company_ticker = re.findall('data-drug-title="(.+?)"',line)
		
	company_ticker = company_ticker[0].split(':')
	
	company_ticker = company_ticker[0]
	
	# PULL DRUG TITLE & PHASE
	drug_title = re.findall('<td style="width: 20%">(.+?)<',line)

	# PHASE LOGIC
	phase = re.findall('data-value="(.+?)"',line)
	
	if len(phase) == 0:
		phase = 'BLANK'
		
	else:
		phase = phase[0]	
	
	# PULL INDICATION & LOGIC IF NULL RETURNED TO ALTERNATIVE VALUE
	indication_1 = re.findall('data-indications="(.+?)"',line)
	
	indication_2 = re.findall('<td style="width: 20%">(.+?)<',line)
	
	if len(indication_1) == 0:
		indication = indication_2[0]
		
	else:
		indication = indication_1	
	
	# STOCK DETAILS
	try:
		
		details = re.findall('<td style="width: 30%"><a href="(.+?)<',line)
		
		details = details[0].split('>')
		
		details = details[1]
	
	except:
		continue
	
	# CREATE DATAFRAME
	data_line = {'Ticker': company_ticker,
				'Drug_Title': drug_title[0],
				'Indications': indication[0],
				'Phase': phase,
				'Details': details
				}
	
	df = pd.DataFrame(data = data_line,index = [count])
	
	finaldf = pd.concat([finaldf,df], axis = 0)
	
	print (df)
	print ('')
	
	count = count + 1

#----------------------------------------------------------------
# PHASE CONVERTER

def phase_transform (row):

	if row == 'approved':
		row = 1

	elif row == 'ndaFiling':
		row = 2
		
	elif row == 'blaFiling':
		row = 3

	elif row == 'sndaFiling':
		row = 4
		
	elif row == 'crl':
		row = 5
		
	elif row == 'pdufaPriorityReview':
		row = 6

	elif row == 'pdufa':
		row = 7

	elif row == 'phase3':
		row = 8

	elif row == 'phase23':
		row = 9

	elif row == 'phase2b':
		row = 10

	elif row == 'phase2':
		row = 11

	elif row == 'phase2a':
		row = 12

	elif row == 'phase1b':
		row = 13

	elif row == 'phase1.5':
		row = 14

	elif row == 'phase1':
		row = 15

	elif row == 'phase1a':
		row = 16
		
	else: 
		row = 17
		
	return (row)
			
finaldf['Phase_Rank'] = finaldf['Phase'].apply(lambda row: phase_transform(row))

print (finaldf)

# SQL-------------------------------

# CREATE DATABASE TO STORE DATA
conn = sqlite3.connect('Stock_list.sqlite')
cur = conn.cursor()
cur.execute('''PRAGMA journal_mode = OFF''')
cur.execute('DROP TABLE IF EXISTS drugs')

finaldf.to_sql('drugs',conn,if_exists = 'append')



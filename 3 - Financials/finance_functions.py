import sqlite3
import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import numpy as np

def req(url):
    proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support) 
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(url).read()

print req('http://google.com')

'''
def market_cap_f (ticker):

	# PICK INCOME, BALANCE SHEET, OR CASHFLOW

	url = 'https://www.nasdaq.com/symbol/' + ticker
		
	# OPEN URL

	html = urllib.request.urlopen(url).read()

	html = html.decode()

	table = html.split('Market Cap')
	
	table = table[1]
	
	company_market_cap = re.findall('<div class="table-cell">(.?+)',table[6])

	return (company_market_cap)
'''

    

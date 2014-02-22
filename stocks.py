### Stocks
### Sean Welleck | 2014
#
# A module for retrieving stock information using the
# yahoo finance API (https://code.google.com/p/yahoo-finance-managed/wiki/CSVAPI)

import csv
import urllib2

# Retrieves the stock quote for the given symbol
# from Yahoo Finance as a float.
# Input:  symbol - stock symbol as a string
# Output: price  - latest trade price from yahoo finance
def get_stock_quote(symbol):
	BASE_URL = 'http://download.finance.yahoo.com/d/quotes.csv?s='
	ID = symbol
	close_prop = '&f=l1'
	SUFFIX = '&e=.csv'
	url = "%s%s%s%s" % (BASE_URL, ID, close_prop, SUFFIX)
	price = float(urllib2.urlopen(url).read().strip())
	return price

# Downloads the stock history for the given symbol,
# for the given date range, as a csv file.
# Input: symbol   - stock symbol as a string
#        start    - start date in the form 'mm/dd/yyyy'
#        end      - end date in the form 'mm/dd/yyyy'
#        outfile  - output filename, e.g. 'out.csv'
#        interval - trading interval; either d, w, m (daily, weekly, monthl7)
def csv_quote_history(symbol, start, end, outfile, interval='d'):
	BASE_URL = 'http://ichart.yahoo.com/table.csv?s='
	ID = symbol
	sm, sd, sy = start.split('/')
	em, ed, ey = end.split('/')
	url = "%s%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=%s" % (BASE_URL, ID, (int(sm)-1), int(sd), int(sy), (int(em)-1), int(ed), int(ey), interval)
	response = urllib2.urlopen(url)
	with open(outfile, 'wb') as f:
		csv_reader = csv.reader(response)
		csv_writer = csv.writer(f)
		for row in csv_reader:
			csv_writer.writerow(row)
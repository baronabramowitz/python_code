#import sys
#sys.path.append('/Users/baronabramowitz/Desktop/finance_0')
#sys.path.append('/Users/baronabramowitz/Desktop/finance_0/finance')
#sys.path.append('/Users/baronabramowitz/Desktop/finance_0/decimalpy')
#import finance

import re
import xlwings as xw
import pandas as pd
import requests
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
from datetime import datetime, date

#import BankDate_ as BD


def build_strips_curve():
	'''
	This function takes an xml format (also works with plain text) from 
	http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices
	and converts it into an excel spreadsheet of spot rates of strips for 
	each strip maturity date. These strips can then be used to generate a 
	yield curve with which different securities can be priced. The use of 
	xlwings to move the data into excel was just an exercise to create 
	a more human readable format without going to the horrors of VBA.
	'''
	data_location = ('http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.'
		'2&page=Gilts/Daily_Prices')
	page = requests.get(data_location)
	if page.status_code==200:
		base_data_location_string = '/Users/baronabramowitz/Desktop/todays_strips_data_raw' + str(datetime.now())
		raw_xml = open(base_data_location_string,'w')
		raw_xml.write('Download Timestamp: ' 
					+ str(datetime.now()) 
					+ page.text)
		raw_xml.close()
	else:
		print("link invalid")

	pattern = re.compile("INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE=\"(2\d{3}[-][0-1][0-9][-][0-3][0-9])T.{157}YIELD=\"(\d{1,2}\.\d{12}\")")
	pattern_g1_matches = []
	pattern_g2_matches = []
	match_list = []
	for i, line in enumerate(open('/Users/baronabramowitz/Desktop/todays_'
		'strips_data_raw')): 

	    for match in re.finditer(pattern, line):
	    	match_list.append(match)
	    	pattern_g1_matches.append(match.group(1))
	    	pattern_g2_matches.append(match.group(2)[:-1])

	pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
	pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
	strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df,
							 left_index=True, right_index = True)
	strips_output.columns = ['Date','Yield']
	strips_output['Date'] = pd.to_datetime(strips_output['Date'])
	strips_output = strips_output.sort_values('Date')
	days_to_maturity = [(mat_date - datetime.today()).days for mat_date in strips_output['Date']]
	days_to_mat_series = pd.Series(days_to_maturity)
	strips_output['Days to Maturity'] = days_to_mat_series.values
	strips_output.index = range(0,len(strips_output))
	strips_output = strips_output.drop_duplicates('Date', keep = 'last')
	#print(strips_output)
	x1 = strips_output['Days to Maturity']
	y1 = strips_output['Yield']
	spl = InterpolatedUnivariateSpline(x1, y1)
	plt.plot(x1, y1, 'ro', ms=5)
	xs = np.linspace(min(x1), max(x1), 1000)
	#spl_output = spl(xs)
	#print(spl_output)
	plt.plot(xs, spl(xs), 'g', lw=3, alpha=0.7)
	plt.xlabel('Days to Maturity')
	plt.ylabel('Yield')
	plt.show()
	
			#Input any Excel output file you'd like, but it makes most sense 
			#to put it on a new sheet
	"""
	wb = xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx')
	wb.sheets('Sheet1').range('A1').value = strips_output
	wb.sheets('Sheet1').range('A1').options(pd.DataFrame, expand='table').value
	wb.sheets('Sheet1').range('D:D').value = None
	#Chart built from next four lines
	chart = wb.sheets('Sheet2').charts.add()
	chart.set_source_data(wb.sheets('Sheet1').range('B1').expand())
	chart.chart_type = 'line'
	chart.name = 'Yield Curve'
	"""


if __name__ == "__main__":
	build_strips_curve()

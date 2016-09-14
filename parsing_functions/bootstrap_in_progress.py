

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


def bootstrap_curve():
	'''
	This function takes an xml format (also works with plain text) from 
	http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices
	and converts it into an excel spreadsheet of cupon bond yields. 
	These yields can be bootstrapped into a yield curve with which different 
	securities can be priced. The use of xlwings to move the data into excel 
	was just an exercise to create a more human readable format without going 
	to the horrors of VBA.
	'''
data_location = ('http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.'
	'2&page=Gilts/Daily_Prices')
page = requests.get(data_location)
if page.status_code==200:
	# Downloads raw xml
	base_data_location_string = '/Users/baronabramowitz/Desktop/todays_bootstrap_data_raw' + str(datetime.now())
	raw_xml = open(base_data_location_string,'w')
	raw_xml.write('Download Timestamp: ' 
				+ str(datetime.now()) 
				+ page.text)
	raw_xml.close()
	raw_xml = open(base_data_location_string,'r+')
	# Replaces unicode vulgar fractions with decimals
	# Shouldn't really be hardcoded but it was the most expedient
	FRACTIONS = {
    u'\u00BD' : .5,
    u'\u00BC' : .25,
    u'\u00BE' : .75,
    u'\u2153' : .333333333333,
    u'\u2154' : .666666666667,
    u'\u2155' : .2,
    u'\u2156' : .4,
    u'\u2157' : .6,
    u'\u2158' : .8,
    u'\u2159' : .166666666667,
    u'\u215A' : .833333333333,
    u'\u215B' : .125,
    u'\u215C' : .375,
    u'\u215D' : .625,
    u'\u215E' : .875,
	}
	FRACTIONS = dict((re.escape(k), str(v)[1:]) for k, v in FRACTIONS.items())
	pattern1 = re.compile("|".join(FRACTIONS.keys()))
	text = pattern1.sub(lambda m: FRACTIONS[re.escape(m.group(0))], raw_xml.read())
	raw_xml.seek(0)
	raw_xml.write(text)
	raw_xml.truncate()
	raw_xml.close()
	pattern2 = re.compile("INSTRUMENT_NAME=\"([\d]{1,2}\.?[\d]{0,12})[%] Treasury Gilt 20[\d]{2}\" REDEMPTION_DATE=\"(2\d{3}[-][0-1][0-9][-][0-3][0-9]).{158,160}YIELD=\"([\d]{1,2}\.[\d]{12})")
	pattern_g1_matches = []
	pattern_g2_matches = []
	pattern_g3_matches = []
	match_list = []
	for match in re.finditer(pattern2, open(base_data_location_string, 'r').read()):
		match_list.append(match)
		pattern_g1_matches.append(match.group(1))
		pattern_g2_matches.append(match.group(2))
		pattern_g3_matches.append(match.group(3))

	pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
	pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
	pattern_g3_matches_df = pd.DataFrame(pattern_g3_matches)

	bootstrap_output = pd.merge(pd.merge(pattern_g2_matches_df,pattern_g1_matches_df,
							 left_index=True, right_index = True),
						pattern_g3_matches_df,left_index=True, right_index = True)

	bootstrap_output.columns = ['Date','Coupon','Yield']
	bootstrap_output['Date'] = pd.to_datetime(bootstrap_output['Date'])
	bootstrap_output = bootstrap_output.sort_values('Date')
	days_to_maturity = []
	for mat_date in bootstrap_output['Date']:
		dtm = (mat_date - datetime.today()).days
		days_to_maturity.append(dtm)
	days_to_mat_series = pd.Series(days_to_maturity)
	bootstrap_output['Days to Maturity'] = days_to_mat_series.values
	bootstrap_output.index = range(0,len(bootstrap_output))
	bootstrap_output = bootstrap_output.drop_duplicates('Date', keep = 'last')

	print(bootstrap_output)

				#Input any Excel output file you'd like, but it makes most sense 
			#to put it on a new sheet
	wb = xw.Book(r'/Users/baronabramowitz/Desktop/bootstrap_testing.xlsx')
	wb.sheets('Sheet1').range('A1').value = bootstrap_output
	wb.sheets('Sheet1').range('A1').options(pd.DataFrame, expand='table').value
	wb.sheets('Sheet1').range('E:E').value = None
	#Chart built from next four lines
	chart = wb.sheets('Sheet2').charts.add()
	chart.set_source_data(wb.sheets('Sheet1').range('B1').expand())
	chart.chart_type = 'line'
	chart.name = 'Yield Curve'

else:
	print("link invalid")



	"""
	x1 = bootstrap_output['Days to Maturity']
	y1 = bootstrap_output['Yield']
	spl = InterpolatedUnivariateSpline(x1, y1)
	plt.plot(x1, y1, 'ro', ms=5)
	xs = np.linspace(min(x1), max(x1), 1000)
	#spl_output = spl(xs)
	#print(spl_output)
	plt.plot(xs, spl(xs), 'g', lw=3, alpha=0.7)
	plt.show()
	"""




if __name__ == "__main__":
	bootstrap_curve()

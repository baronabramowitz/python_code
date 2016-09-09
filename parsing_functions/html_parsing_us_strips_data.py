import re
import xlwings as xw
import pandas as pd
import numpy as np
import requests
import scipy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
from datetime import datetime, date

def generate_yield_curve_data():
	'''
	This function takes an html format (also works with plain text) from 
	http://online.barrons.com/mdc/public/page/9_3020-tstrips.html?mod=bol_topnav_9_3000
	and converts it into an excel spreadsheet of spot rates of strips for each strip maturity date. 
	These strips can then be used to generate a yield curve with which different securities can be priced.
	The use of xlwings t move the data into excel was just an exercise to create a more human readable format 
	without going to the horrors of VBA
	'''
	page = requests.get('http://online.barrons.com/mdc/public/page/9_3020-tstrips.html?mod=bol_topnav_9_3000')
	if page.status_code==200:
		base_data_location_string = '/Users/baronabramowitz/Desktop/todays_us_strips_data_raw' + str(datetime.now())
		raw_xml = open(base_data_location_string,'w')
		raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)			
		raw_xml.close()
	else:
		print("link invalid")

	pattern_date = re.compile(r"<td class=\"text\">(2[0-9]{3} [a-zA-z]{3} [0-3][0-9])</td>")
	pattern_yield = re.compile(r"<td style=\"border-right:0px\" class=\"num\">([0-9]{1,2}\.[0-9]{2})</td>")
	pattern_g1_matches = []
	pattern_g2_matches = []
	match_list = []
	for i, line in enumerate(open(base_data_location_string, 'r')): 
		if i > 2480:
			for match in re.finditer(pattern_date, line):
				match_list.append(match)
				pattern_g1_matches.append(match.group(1))
		else:
			pass

	for i, line in enumerate(open(base_data_location_string, 'r')):
		if i > 2480:
			for match in re.finditer(pattern_yield, line):
				match_list.append(match)
				pattern_g2_matches.append(match.group(1))
		else:
		    pass

	pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
	pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
	strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df, left_index=True, right_index = True)
	strips_output.columns = ['Date','Yield']
	strips_output['Date'] = pd.to_datetime(strips_output['Date'])
	strips_output = strips_output.sort_values('Date')
	days_to_maturity = []
	for mat_date in strips_output['Date']:
		dtm = (mat_date - datetime.today()).days
		days_to_maturity.append(dtm)
	days_to_mat_series = pd.Series(days_to_maturity)
	strips_output['Days to Maturity'] = days_to_mat_series.values
	strips_output.index = range(0,len(strips_output))
	x1 = strips_output['Days to Maturity']
	y1 = strips_output['Yield']
	spl = InterpolatedUnivariateSpline(x1, y1)
	plt.plot(x1, y1, 'ro', ms=5)
	xs = np.linspace(min(x1), max(x1), len(strips_output))
	plt.plot(xs, spl(xs), 'g', lw=3, alpha=0.7)
	plt.show()


			#Input any Excel output file you'd like, but it makes most sense to put it on a new sheet
	xw.Book('/Users/baronabramowitz/Desktop/us_bond_yield_data_and_curve.xlsx').sheets('Sheet1').range('A1').value = strips_output
	xw.Book('/Users/baronabramowitz/Desktop/us_bond_yield_data_and_curve.xlsx').sheets('Sheet1').range('A1').options(pd.DataFrame, expand='table').value
	#Chart built from next four lines
	chart = xw.Book('/Users/baronabramowitz/Desktop/us_bond_yield_data_and_curve.xlsx').sheets('Sheet2').charts.add()
	chart.set_source_data(xw.Book('/Users/baronabramowitz/Desktop/us_bond_yield_data_and_curve.xlsx').sheets('Sheet1').range('B1').expand())
	chart.chart_type = 'line'
	chart.name = 'Yield Curve'
	return strips_output

if __name__ == "__main__":
	generate_yield_curve_data()
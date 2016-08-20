import re
import xlwings as xw
import pandas as pd
import requests
from datetime import datetime

def generate_yield_curve_data():
	#page = requests.get('http://www.barrons.com/public/page/9_0210-govtstrips.html')
	page = requests.get('http://online.barrons.com/mdc/public/page/9_3020-tstrips.html?mod=bol_topnav_9_3000')
	if page.status_code==200:
		base_data_location_string = '/Users/baronabramowitz/Desktop/todays_us_strips_data_raw' + str(datetime.now())
		raw_xml = open(base_data_location_string,'w')
		raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)			
		raw_xml.close()
	else:
		print("link invalid")

#"<td align=\"center\"><font id=\"standard\">([a-zA-z]{3} [0-6][0-9]).{50}ci.{194}<font id=\"standard\">([0-9]{1,2}\.[0-9]{2})</font></td>"
	#pattern = re.compile("<td align=\"center\"><font id=\"standard\">([a-zA-z]{3} [0-6][0-9]).{50}ci.{194}<font id=\"standard\">([0-9]{1,2}\.[0-9]{2})</font></td>")
#"<td class=\"text\">(2\d{3} [a-zA-z]{3} [0-3][0-9]).{121}\"num\">([0-9]{1,2}\.[0-9]{2})</td>"
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
	print (match_list)
	print (pattern_g1_matches)
	print (pattern_g2_matches)
	pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
	pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
	strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df, left_index=True, right_index = True)
	strips_output.columns = ['Date','Yield']
	strips_output['Date'] = pd.to_datetime(strips_output['Date'])
	strips_output = strips_output.sort_values('Date')
	strips_output.index = range(0,len(strips_output))
	#print(strips_output)

			#Input any Excel output file you'd like, but it makes most sense to put it on a new sheet
			#r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx'
	#excel_output_location = r'/Users/baronabramowitz/Desktop/xlwings_testing_doc'+str(datetime.now())+'.xlsx'
	#xw.Book().save(excel_output_location)
	#xw.Book(excel_output_location).sheets('Sheet1').range('A1').value = strips_output
	#xw.Book(excel_output_location).sheets('Sheet1').range('A1').options(pd.DataFrame, expand='table').value
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
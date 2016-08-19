import re
import xlwings as xw
import pandas as pd

def test_xml():
	'''
	This function takes an XML format (also works with plain text) from http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices
	and converts it into an excel spreadsheet of spot rates of strips for each strip maturity date. 
	These strips can then be used to generate a yield curve with which different securities can be priced.
	The use of xlwings t move the data into excel was just an exercise to create a more human readable format 
	without going to the horrors of VBA
#"INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE="(2\d{3}-\d{2}-\d{2})T.{157}YIELD=\"(\d{1,2}\.\d{12}\")
#"INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE="(2\d{3}-\d{2}-\d{2})T.{157}YIELD=\"(\d{1,2}\.\d{12}\")"
	'''
	pattern = re.compile("INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE=\"(2\d{3}[-][0-1][0-9][-][0-3][0-9])T.{157}YIELD=\"(\d{1,2}\.\d{12}\")")
	pattern_g1_matches = []
	pattern_g2_matches = []
	match_list = []
	for i, line in enumerate(open('/Users/baronabramowitz/Desktop/<SILO_DAILY_PRICES ISIN_CODE="GB0000514405" INSTRU.xml')): #Feed XML output as text here.
	    for match in re.finditer(pattern, line):
	    	match_list.append(match)
	    	pattern_g1_matches.append(match.group(1))
	    	pattern_g2_matches.append(match.group(2)[:-1])

	#print (match_list)
	#print (pattern_g1_matches)
	#print (pattern_g2_matches)
	pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
	pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
	strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df, left_index=True, right_index = True)
	strips_output.columns = ['Date','Yield']
	strips_output['Date'] = pd.to_datetime(strips_output['Date'])
	strips_output = strips_output.sort_values('Date')
	strips_output.index = range(0,len(strips_output))
	#print(strips_output)

			#Input any Excel output file you'd like, but it makes most sense to put it on a new sheet
	xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet3').range('A1').value = strips_output
	xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet3').range('A1').options(pd.DataFrame, expand='table').value
	#Chart built from next four lines
	chart = xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet4').charts.add()
	chart.set_source_data(xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet3').range('B1').expand())
	chart.chart_type = 'line'
	chart.name = 'Yield Curve'


if __name__ == "__main__":
	test_xml()

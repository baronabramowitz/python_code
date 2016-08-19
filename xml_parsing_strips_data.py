import re
import xlwings as xw
import pandas as pd

def test_xml():
	'''
	This function takes an xml format as text from http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices
	and converts it into an excel spreadsheet of spot rates of strips for each strip maturity date. 
	These strips can then be used to generate a yield curve with which different securities can be priced.
	The use of xlwings t move the data into excel was just an exercise to create a more human readable format 
	without going to the horrors of VBA
	'''
	pass
	pattern = re.compile("INSTRUMENT_NAME=\"Treasury Coupon Strip (\d{2}[a-zA-Z]{3}2\d{3}\").{186}YIELD=\"(\d{1,2}\.\d{12}\")")
	pattern_g1_matches = []
	pattern_g2_matches = []
	match_list = []
	for i, line in enumerate(open('/Users/baronabramowitz/Desktop/xml_as_plain_text')): #Feed XML output as text here.
	    for match in re.finditer(pattern, line):
	    	match_list.append(match)
	    	pattern_g1_matches.append(match.group(1)[:-1])
	    	pattern_g2_matches.append(match.group(2)[:-1])

	print (match_list)
	print (pattern_g1_matches)
	print (pattern_g2_matches)
	pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
	pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)

			#Input any Excel output file you'd like, but it makes most sense to put it on a new sheet
	xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet1').range('A1').value = pattern_g1_matches_df
	xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet1').range('A1').options(pd.DataFrame, expand='table').value
	xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet1').range('C1').value = pattern_g2_matches_df
	xw.Book(r'/Users/baronabramowitz/Desktop/xlwings_testing_doc.xlsx').sheets('Sheet1').range('C1').options(pd.DataFrame, expand='table').value

if __name__ == "__main__":
	test_xml()





'''from xml.etree import ElementTree as ET
for line in 
ET.fromstring(line).text'''

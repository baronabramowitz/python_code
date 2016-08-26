import timeit

def build_strips_curve():

	data_location = ('http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.'
		'2&page=Gilts/Daily_Prices')
	page = requests.get(data_location)
	if page.status_code==200:
		raw_xml = open(('/Users/baronabramowitz/Desktop/todays_'
			'strips_data_raw'),'w')
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
	strips_output.index = range(0,len(strips_output))
	return strips_output

if __name__ == "__main__":
	t = timeit.Timer('build_strips_curve()','import xml_parsing_strips_data')   
	#t.timeit()
	t.repeat(3, 10)   






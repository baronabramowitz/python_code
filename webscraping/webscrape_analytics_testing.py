import requests
import textrazor
import webhose
from bs4 import BeautifulSoup
from datetime import datetime

#webhose_api_key = '911521cc-3d9f-4d25-a8c1-c687158a2b32'
#textrazor_api_kei = '0cccf5d913c80e557758ac26850f76992a71924ad031a217b0e5883e'

def query_analytics():
	search_input = str(input('What are the company query parameters?   '))
	webhose.config('911521cc-3d9f-4d25-a8c1-c687158a2b32')
	webhose_response = webhose.search(search_input).posts
	url_list_omgili = []
	url_list = []
	for post in webhose_response:
		url_list_omgili.append(post.url)
	for url in url_list_omgili:
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "lxml")
		metatag = soup.find('meta', attrs={'http-equiv': 'refresh'})
		url = (metatag['content']).partition('=')[2]
		url_list.append(url)
	for url in url_list:
		page_analytics(url)

def page_analytics(url):
	print(url)
	page = requests.get(url)
	#soup = BeautifulSoup(page.text, "lxml")
	#print(soup.prettify())
	
	if page.status_code==200:
		#base_data_location_string = '/Users/baronabramowitz/Desktop/beautifulsoup_testing' + str(datetime.now())
		#raw_xml = open(base_data_location_string,'w')
		#raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)			
		#raw_xml.close()
		soup = BeautifulSoup(page.text, "lxml")
		content = []
		try:
			content.append(soup.find('title').text)
		except:
			print ('no beautifulsoup content')
		for p in soup.find_all('p'):
			content.append(p.get_text())
		page_text = " ".join(content)

		textrazor.api_key = "0cccf5d913c80e557758ac26850f76992a71924ad031a217b0e5883e"

		client = textrazor.TextRazor(extractors=["entities", "topics"])
		try:
			response = client.analyze(page_text)
			#print(response.topic.label, response.topic.score)
			for entity in response.entities():
				if entity.relevance_score > .5 :
					print (entity.id, entity.relevance_score, entity.confidence_score)#, entity.freebase_types)
				else:
					pass
		except:
			print('Oops!')
	
	else:
		print("link invalid")
	

if __name__=='__main__':
	query_analytics()
    #from timeit import Timer
    #t = Timer("test()", "from __main__ import test")
    #print(t.timeit(10))


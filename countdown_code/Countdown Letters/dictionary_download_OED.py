__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '25/08/2016'

import requests
page = requests.get('https://raw.githubusercontent.com/sujithps/Dictionary/master/Oxford%20English%20Dictionary.txt')
raw_xml = open(('/Users/baronabramowitz/Desktop/dictionary_file_OED'),'w')
raw_xml.write(page.text)
raw_xml.close()
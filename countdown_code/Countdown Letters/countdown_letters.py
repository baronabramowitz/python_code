__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '25/08/2016'

import re
letters = input('What are the letters?  ')
wcl = [letters.count(letter) for letter in [chr(i) for i in range(ord('a'),ord('z')+1)]]


regex_input = r'\W([' + re.escape(letters) + r']{5,9})\W'
pattern = re.compile(regex_input)
match_list = []
# List of all words containint letters from the input
delete_list = []
# List of words within match_list that exceed the number of letters available 
for i, line in enumerate(open('/Users/baronabramowitz/Desktop/python_code/countdown_code/Countdown Letters/dictionary_file_OED')): 
    for match in re.finditer(pattern, line):
    	match_list.append(match.group(1))
match_list = list(set(match_list))
for word in match_list:
	if (
		wcl[0] < word.count('a') or wcl[1] < word.count('b') or
		wcl[2] < word.count('c') or wcl[3] < word.count('d') or
		wcl[4] < word.count('e') or wcl[5] < word.count('f') or
		wcl[6] < word.count('g') or wcl[7] < word.count('h') or
		wcl[8] < word.count('i') or wcl[9] < word.count('j') or
		wcl[10] < word.count('k') or wcl[11] < word.count('l') or
		wcl[12] < word.count('m') or wcl[13] < word.count('n') or 
		wcl[14] < word.count('o') or wcl[15] < word.count('p') or
		wcl[16] < word.count('q') or wcl[17] < word.count('r') or
		wcl[18] < word.count('s') or wcl[19] < word.count('t') or
		wcl[20] < word.count('u') or wcl[21] < word.count('v') or
		wcl[22] < word.count('w') or wcl[23] < word.count('x') or
		wcl[24] < word.count('y') or wcl[25] < word.count('z')):
		delete_list.append(word)
	else:
		pass
for word in delete_list:
    match_list.remove(word)
match_list.sort(key = len)
print ('One:   ',match_list[len(match_list)-1],'(',len(match_list[len(match_list)-1]),')')
print ('Two:   ',match_list[len(match_list)-2],'(',len(match_list[len(match_list)-2]),')')
print ('Three: ',match_list[len(match_list)-3],'(',len(match_list[len(match_list)-3]),')')
print ('Four:  ',match_list[len(match_list)-4],'(',len(match_list[len(match_list)-4]),')')
print ('Five:  ',match_list[len(match_list)-5],'(',len(match_list[len(match_list)-5]),')')

   
__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

import csv
import json
import pandas as pd
import numpy as np
import psycopg2


def portfolio_sql_insert(csv_location):
	"""Inserts JSON objects into PostgreSQL database from a csv of bonds"""

	try:
	    conn = psycopg2.connect("dbname='fi_data' user='pyconnect' host='localhost' password='pypwcon'")
	except:
	    print ("I am unable to connect to the database")

	portfolio = pd.read_csv(csv_location,
							header = 0,
							delimiter = ',',
							converters = {'face_value':np.float64,'maturity_date':str,'coupon_rate':np.float64,
                                         'payments_per_year':np.float64,'rating':str,'btype':str
                                         }
                          	)
	portfolio = portfolio.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', 
		double_precision = 10, force_ascii = True, date_unit = 'ms', default_handler = None)
	print(portfolio)
	
def json_insert(csv_location):
	try:
	    conn = psycopg2.connect("dbname='fi_data' user='pyconnect' host='localhost' password='pypwcon'")
	except:
	    print ("I am unable to connect to the database")

	cur = conn.cursor()

	#cur.execute("CREATE TABLE bond_data (bond_id serial PRIMARY KEY, bond_json jsonb)")
	cur.execute("SELECT * FROM bond_data")

	for lin in open ('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv.json', 'r+'):
		SQL = "INSERT INTO bond_data (bond_json) VALUES (%s)"
		data = [(lin)]
		cur.execute(SQL, data)

	cur.execute("SELECT * FROM bond_data")
	conn.commit()
	print (cur.fetchall())
	cur.close()
	conn.close()


def sql_query():
	try:
	    conn = psycopg2.connect("dbname='fi_data' user='pyconnect' host='localhost' password='pypwcon'")
	except:
	    print ("I am unable to connect to the database")

	cur = conn.cursor()
	cur.execute("SELECT * FROM bond_data")



def json_generation(csv_location):
	"""Generates a file of JSON objects from """
	csvfile = open(csv_location, 'r')
	jsonfile = open(csv_location + '.json', 'w')
	fieldnames = ('face_value', 'maturity_date',	'coupon_rate', 'payments_per_year', 'rating','type')
	reader = csv.DictReader( csvfile, fieldnames)
	for row in reader:
	    json.dump(row, jsonfile)
	    jsonfile.write('\n')

if __name__ == "__main__":
	#sql_query()
	#portfolio_sql_insert('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
	#json_generation('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
	json_insert('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv.json')

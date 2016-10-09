__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

"""Portfolio Generation Code"""

import pandas as pd
import numpy as np
import psycopg2
import bond_class as bc

def generate_portfolio(csv_location):
	    """Generate portfolio list of Bond objects from the CSV at the inputted location"""

	    portfolio = pd.read_csv(csv_location,
	                           header = 0,
	                           delimiter = ',',
	                           converters = {'face_value':np.float64,'maturity_date':str,'coupon_rate':np.float64,
	                                         'payments_per_year':np.float64,'rating':str,'btype':str
	                            }
	    )
	    for row in portfolio.itertuples():
	    	print (row[1:])
	    portfolio = [bc.Bond(*row[1:]) for row in portfolio.itertuples()]
	    return portfolio

def generate_portfolio_psql():
	try:
	    conn = psycopg2.connect("dbname='fi_data' user='your_user' host='localhost' password='your_pw'")
	except:
	    print ("I am unable to connect to the database")
	conn = psycopg2.connect("dbname='fi_data' user='your_user' host='localhost' password='your_pw'")
	cur = conn.cursor()
	cur.execute("SELECT * FROM bond_data")
	portfolio = [bc.Bond(*tuple((d[1]['face_value'],d[1]['maturity_date'],d[1]['coupon_rate'],
								d[1]['payments_per_year'],d[1]['rating'],d[1]['type']))) for d in cur.fetchall()]
	print (portfolio)
	cur.close()
	conn.close()

class Portfolio(object):
	"""A portfolio class that contains a set of Bond objects"""
	def __init__(self, csv_location):
		self.contents = generate_portfolio(csv_location)
	
	def value(self):
		"""Generate the value the portfolio"""
		return sum([bond.value() for bond in self.contents])

	def contents_value(self):
		"""Generate the value of each bond in the portfolio"""
		return [bond.value() for bond in self.contents]

	def contents_maturity(self):
		"""Generate the maturity in years of each bond in the portfolio"""
		return [bond.maturity_remaining() for bond in self.contents]

	def duration(self):
		"""Generate the duration the portfolio"""
		return sum([(bond.duration()*bond.value())/self.value() for bond in self.contents])

	def contents_duration(self):
		"""Generate the duration contribution of each bond in the portfolio"""
		return [(bond.duration()*bond.value())/self.value() for bond in self.contents]

	def modified_duration(self):
		"""Generate the modified duration the portfolio"""
		return sum([(bond.modified_duration()*bond.value())/self.value() for bond in self.contents])

	def contents_modified_duration(self):
		"""Generate the modified duration contribution of each bond in the portfolio"""
		return [(bond.modified_duration()*bond.value())/self.value() for bond in self.contents]

	def convexity(self):
		"""Generate the convexity the portfolio"""
		return sum([(bond.convexity()*bond.value())/self.value() for bond in self.contents])

	def contents_convexity(self):
		"""Generate the convexity contribution of each bond in the portfolio"""
		return [(bond.convexity()*bond.value())/self.value() for bond in self.contents]


	

if __name__ == "__main__":
	generate_portfolio_psql()
	#generate_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
	"""portfolio = Portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
	print(portfolio.value())
	print(portfolio.duration())
	print(portfolio.convexity())"""
		

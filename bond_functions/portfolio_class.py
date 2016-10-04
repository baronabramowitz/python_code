__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '04/10/2016'

"""Portfolio Generation Code"""

import pandas as pd
import numpy as np
import bond_class as bc

def generate_portfolio(csv_location):
	    """Generates portfolio DataFrame from the CSV at the inputted location"""

	    portfolio = pd.read_csv(csv_location,
	                           header = 0,
	                           delimiter = ',',
	                           converters = {'face_value':np.float64,'maturity_date':str,'coupon_rate':np.float64,
	                                         'payments_per_year':np.float64,'rating':str,'btype':str
	                            }
	    )
	    portfolio = [bc.Bond(*row[1:]) for row in portfolio.itertuples()]
	    return portfolio

class Portfolio(object):
	def __init__(self, csv_location):
		self.contents = generate_portfolio(csv_location)
	
	def value(self):
		return sum([bond.value() for bond in portfolio.contents])

	def contents_value(self):
		"""Generates the value of each bond in the portfolio"""
		return [bond.value() for bond in portfolio.contents]

	def contents_maturity(self):
		"""Generates the maturity in years of each bond in the portfolio"""
		return [bond.maturity_remaining() for bond in portfolio.contents]

	def duration(self):
		return sum([(bond.duration()*bond.value())/self.value() for bond in portfolio.contents])

	def contents_duration(self):
		"""Generates the duration contribution of each bond in the portfolio"""
		return [(bond.duration()*bond.value())/self.value() for bond in portfolio.contents]

	def modified_duration(self):
		return sum([(bond.modified_duration()*bond.value())/self.value() for bond in portfolio.contents])

	def contents_modified_duration(self):
		"""Generates the modified duration contribution of each bond in the portfolio"""
		return [(bond.modified_duration()*bond.value())/self.value() for bond in portfolio.contents]

	def convexity(self):
		return sum([(bond.convexity()*bond.value())/self.value() for bond in portfolio.contents])

	def contents_convexity(self):
		"""Generates the convexity contribution of each bond in the portfolio"""
		return [(bond.convexity()*bond.value())/self.value() for bond in portfolio.contents]


	

if __name__ == "__main__":
	portfolio = Portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
	print(portfolio.convexity())
	print(portfolio.contents_convexity())
		

__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

"""Portfolio Generation Code"""

import pandas as pd
import numpy as np
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
	    portfolio = [bc.Bond(*row[1:]) for row in portfolio.itertuples()]
	    return portfolio

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
	portfolio = Portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
	print(portfolio.value())
	print(portfolio.duration())
	print(portfolio.convexity())
		

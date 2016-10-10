__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

"""Portfolio Generation Code"""

import pandas as pd
import numpy as np
import psycopg2
import bond_class as bc
import var_scenario_gen as vsg
import babel.numbers
import decimal
from datetime import datetime

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

def generate_portfolio_psql(bond_set):
	try:
	    conn = psycopg2.connect("dbname='fi_data' user='your_user' host='localhost' password='your_pw'")
	except:
	    print ("I am unable to connect to the database")
	conn = psycopg2.connect("dbname='fi_data' user='your_user' host='localhost' password='your_pw'")
	cur = conn.cursor()
	if bond_set == 'All':
		cur.execute("SELECT * FROM bond_data")
	elif bond_set == 'Corporate':
		cur.execute("SELECT * FROM bond_data WHERE bond_json ->> 'type' = 'Corporate'")
	elif bond_set == 'Government':
		cur.execute("SELECT * FROM bond_data WHERE bond_json ->> 'type' = 'Government'")
	else:
		print('What you doing mate?')
	portfolio = [bc.Bond(*tuple((d[1]['face_value'],d[1]['maturity_date'],d[1]['coupon_rate'],
								d[1]['payments_per_year'],d[1]['rating'],d[1]['type']))) for d in cur.fetchall()]
	cur.close()
	conn.close()
	return portfolio

class Portfolio(object):
	"""A portfolio class that contains a set of Bond objects"""
	def __init__(self, bond_set, currency, var_day_count, var_subsample_fraction, var_percentile):
		#self.contents = generate_portfolio(csv_location)
		self.contents = generate_portfolio_psql(bond_set)
		self.currency = currency
		self.var_horizon = var_day_count
		self.var_subsample_fraction = var_subsample_fraction
		self.var_percentile = var_percentile
	
	def value(self):
		"""Generate the value the portfolio"""
		return sum([bond.value() for bond in self.contents])
		#return babel.numbers.format_currency(decimal.Decimal(str(sum([bond.value() for bond in self.contents]))), self.currency)

	def value_VaR(self,scenario_spl):
		"""Generate the value the portfolio"""
		return sum([bond.value_VaR(scenario_spl) for bond in self.contents])

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

	def VaR(self):
		"""Generate the Value at Risk for the portfolio

		Uses a subset of historical yield curve shifts to model possible yield curve movements.
		Return the percentile specified of the set of loss scenarios as both a formatted value and 
		a percentage of portfolio value.
		Takes an age to compute.
		Increasing the subsample fraction will make the results more consistent and accurate 
		but will also tremendously increase the time it takes to calculate.
		Will likely improve with parallel computing of each VaR calculation within the set
		of scenarios; this should cut down the time but by how much I don't know.
		"""
		var_scenarios = vsg.var_strips_data_generation(self.var_horizon, self.var_subsample_fraction, self.currency)
		# Above takes roughly 2 minutes
		print(datetime.now(), 'Estimated time remaining: ', divmod(((len(var_scenarios)) * 5), 60) )
		VaR_value_set = np.array([self.value_VaR(scenario_spl) for scenario_spl in var_scenarios])
		portfolio_value_bottom = np.percentile(VaR_value_set, (1 - (self.var_percentile/100)))
		VaR = self.value() - portfolio_value_bottom
		VaR_formatted = babel.numbers.format_currency(decimal.Decimal(str(VaR)), self.currency)
		VaR_percentile = str((VaR/self.value()) * 100) + '%'
		return {'VaR' : VaR_formatted, 'VaR Percentage' : VaR_percentile }






	

if __name__ == "__main__":
	"""portfolio_a = Portfolio('All', 'USD', 10, .1, 95)
	portfolio_c = Portfolio('Corporate', 'USD', 10, .1, 95)
	portfolio_g = Portfolio('Government', 'USD', 10, .1, 95)
	print('Initiate VaR', datetime.now())
	print(portfolio_a.VaR())
	print('Process Completed', datetime.now())
	"""
	"""
	print(portfolio_c.VaR())
	print(portfolio_g.VaR())
	"""
	
	#print(portfolio_a.value())
	"""
	print(portfolio_a.duration())
	print(portfolio_a.convexity())
	print(portfolio_c.value())
	print(portfolio_c.duration())
	print(portfolio_c.convexity())
	print(portfolio_g.value())
	print(portfolio_g.duration())
	print(portfolio_g.convexity())
	"""


		

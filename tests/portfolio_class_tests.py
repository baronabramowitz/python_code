__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '06/10/2016'

import unittest
import sys
sys.path.append('/Users/baronabramowitz/Desktop/python_code/bond_functions')

from bond_class import Bond
from portfolio_class import Portfolio, generate_portfolio, generate_portfolio_psql


class TestSuiteBondCode(unittest.TestCase):
    """Large Selection of Tests for the bond_stuff_in_progress.py

    I have recently realized that these tests will need to point to fixed data sets for yields 
    as the bond values will change day to day as the yield curves on which they are based move as well.
    In the interim I've simply used ranges ov values to encompas possibilities for changes in the daily yield curve
    """

    def test_portfolio_value(self):
        self.assertTrue(14000000 <= portfolio_test.value() <= 19000000)

    def test_portfolio_duration(self):
        self.assertTrue(10 <= portfolio_test.duration() <= 12)

    def test_portfolio_convexity(self):
        self.assertTrue(100 <= portfolio_test.convexity() <= 140)

    def test_portfolio_var(self):
        self.assertTrue(1 <= float(portfolio_test.value_at_risk(
            '2015-12-25', 10, 1, 95)['VaR Percentage'][:-1]) <= 3)

    # {'var Percentage': '2.20804229906%', 'var': 'US$400,597.70'}

if __name__ == "__main__":
    portfolio_test = Portfolio('All', 'USD')
    unittest.main()

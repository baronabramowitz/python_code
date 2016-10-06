__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '06/10/2016'

import unittest
import sys
sys.path.append('/Users/baronabramowitz/Desktop/python_code/bond_functions')

from bond_class import Bond
from portfolio_class import Portfolio, generate_portfolio


class TestSuiteBondCode(unittest.TestCase):
    """Large Selection of Tests for the bond_stuff_in_progress.py

    I have recently realized that these tests will need to point to fixed data sets for yields 
    as the bond values will change day to day as the yield curves on which they are based move as well.
    In the interim I've simply used ranges ov values to encompas possibilities for changes in the daily yield curve
    """
    portfolio = Portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')

    def test_portfolio_value(self):
        self.assertTrue( 5500000 <= portfolio.value() <= 6500000 )

    def test_portfolio_duration(self):
        self.assertTrue( 10 <= portfolio.duration() <= 12 )

    def test_portfolio_convexity(self):
        self.assertTrue( 130 <= portfolio.convexity() <= 150 )


if __name__ == "__main__":
    portfolio = Portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv')
    unittest.main()
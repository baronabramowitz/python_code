__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '06/10/2016'

import unittest
import sys
sys.path.append('/Users/baronabramowitz/Desktop/python_code/bond_functions')
from bond_class import Bond

class TestSuiteBondCode(unittest.TestCase):
    """Large Selection of Tests for the bond_class.py

    I have recently realized that these tests will need to point to fixed data sets for yields 
    as the bond values will change day to day as the yield curves on which they are based move as well.
    In the interim I've simply used ranges ov values to encompas possibilities for changes in the daily yield curve
    """

    def test_bond_value(self):
        self.assertTrue( 10000 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').value() <= 12000 )

    def test_bond_value_c(self):
        self.assertTrue( 10000 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').value_c() <= 12000 )

    def test_bond_duration(self):
        self.assertTrue( 4 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').duration() <= 6 )

    def test_bond_duration_c(self):
        self.assertTrue( 4 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').duration_c() <= 6 )

    def test_modified_bond_duration(self):
        self.assertTrue( 4 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').modified_duration() <= 6 )

    def test_modified_bond_duration_c(self):
        self.assertTrue( 4 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').modified_duration_c() <= 6 )

    def test_bond_convexity(self):
        self.assertTrue( 0 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').convexity() <= 50 )

    def test_bond_convexity_c(self):
        self.assertTrue( 0 <= Bond(face_value = 10000.0,
                maturity_date = '2022-06-15',
                coupon_rate = 2.5,
                payments_per_year = 2,
                rating = 'AAA',
                btype = 'Corporate').convexity_c() <= 50 )

if __name__ == "__main__":
    unittest.main()
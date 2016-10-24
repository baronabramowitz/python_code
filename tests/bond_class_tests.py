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

    I have recently realized that these tests will need to point to fixed
    data sets for yields as the bond values will change day to day as the
    yield curves on which they are based move as well. In the interim I've
    simply used ranges ov values to encompas possibilities for changes in
    the daily yield curve
    """

    def test_bond_value(self):
        self.assertTrue(10000 <= bond_test.value() <= 12000)

    def test_bond_value_c(self):
        self.assertTrue(10000 <= bond_test.value_c() <= 12000)

    def test_bond_duration(self):
        self.assertTrue(4 <= bond_test.duration() <= 6)

    def test_bond_duration_c(self):
        self.assertTrue(4 <= bond_test.duration_c() <= 6)

    def test_modified_bond_duration(self):
        self.assertTrue(4 <= bond_test.modified_duration() <= 6)

    def test_modified_bond_duration_c(self):
        self.assertTrue(4 <= bond_test.modified_duration_c() <= 6)

    def test_bond_convexity(self):
        self.assertTrue(0 <= bond_test.convexity() <= 50)

    def test_bond_convexity_c(self):
        self.assertTrue(0 <= bond_test.convexity_c() <= 50)

    def test_bond_value_zcb(self):
        self.assertTrue(8000 <= bond_test_zcb.value() <= 12000)

    def test_bond_value_c_zcb(self):
        self.assertTrue(8000 <= bond_test_zcb.value_c() <= 12000)

    def test_bond_duration_zcb(self):
        self.assertTrue(4 <= bond_test_zcb.duration() <= 6)

    def test_bond_duration_c_zcb(self):
        self.assertTrue(4 <= bond_test_zcb.duration_c() <= 6)

    def test_modified_bond_duration_zcb(self):
        self.assertTrue(4 <= bond_test_zcb.modified_duration() <= 6)

    def test_modified_bond_duration_c_zcb(self):
        self.assertTrue(4 <= bond_test_zcb.modified_duration_c() <= 6)

    def test_bond_convexity_zcb(self):
        self.assertTrue(0 <= bond_test_zcb.convexity() <= 50)

    def test_bond_convexity_c_zcb(self):
        self.assertTrue(0 <= bond_test_zcb.convexity_c() <= 50)

if __name__ == "__main__":
    bond_test = Bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate')
    bond_test_zcb = Bond(10000.0, '2022-06-15', 0, 0, 'AAA', 'Corporate')
    # Would make max value face value but with neg int rates, who knows
    # these days
    unittest.main()

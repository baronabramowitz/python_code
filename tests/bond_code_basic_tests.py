__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '22/08/2016'

import unittest
import value_bond as vb
import duration_bond as db
import convexity_bond as cb

class TestSuiteBondCode(unittest.TestCase):
     """Large Selection of Tests for the bond_stuff_in_progress.py"""
     def test_portfolio_VaR(self):
        self.assertEqual({'Portfolio VaR Percent': 6.5004978313881256, 'Portfolio VaR': 417084.6525381055},
            value_at_risk_portfolio_set('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv', 95))
        self.fail("Known Failure")
     def test_bond_convexity(self):
         self.assertEqual({'Bond Convexity': 36.36653523348562},
                cb.convexity_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
     def test_portfoio_convexity(self):
         self.assertEqual({'Portfolio Convexity': 143.72975134873602},
            cb.convexity_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
     def test_duration_portfolio(self):
         self.assertEqual({'Portfolio Duration': 11.093967137303755, 'Modified Portfolio Duration': 11.048514534591584}
            ,db.duration_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
     def test_value_portfolio(self):
         self.assertEqual({'Set of Bond Values': [11320.188859642592, 42745.647831637427, 3902833.9817734361, 
            275809.67525298434, 831588.72828977392, 403632.83643454808, 554517.6557094187, 393746.83512144675], 
            'Set of Bond Maturities': [5.8191780821917805, 8.923287671232877, 12.378082191780821, 1.5753424657534247, 
            7.96986301369863, 17.232876712328768, 11.487671232876712, 10.2], 
            'Portfolio Value': 6416195.5492728874},
            vb.value_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
     def test_bond_dur(self):
        #Checks if bond duration properly calculates
        self.assertEqual({'Modified Duration': 5.447036192738801, 'Bond Duration': 5.455872780654858},
            db.duration_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA','Corporate'))
     def test_bond_val(self):
        #Checks if bond value properly calculates
        self.assertEqual((11321.928444124125, [124.92962437224833, 124.8759248234797, 124.82520284124303, 
            124.76929655187979, 124.69524141994178, 124.59769289760095, 124.46073934338344, 124.27685339815154, 
            124.03101248430148, 123.72361917185522, 123.33685616967725, 9953.406380650362], [116, 298, 481, 663, 
            848, 1030, 1212, 1394, 1577, 1759, 1942, 2124], 5.8191780821917805, [0.17720275999999996, 
            0.12163759999999998, 0.106188285, 0.10170096999999999, 0.10506873999999998, 0.11423621999999999, 
            0.13020216999999998, 0.15191707999999998, 0.180118855, 0.21297338999999998, 0.25175044999999996, 0.29373288]),
        vb.value_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))


if __name__ == "__main__":
    #todays_strips_data = strips_data_generation()
    unittest.main()
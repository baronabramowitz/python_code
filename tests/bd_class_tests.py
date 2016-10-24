__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '24/10/2016'

import unittest
import sys
from datetime import datetime
sys.path.append('/Users/baronabramowitz/Desktop/python_code/bond_functions')
from bankdate import BankDate, date_range


class TestSuiteBankDate(unittest.TestCase):
    """Large Selection of Tests for the bankdate.py

    Used fixed range of dates to mitigate issues with changing 
    relative time deltas across months
    """

    def test_BD_add_y(self):
        self.assertEqual(test_date._add('3y'), comp_date
                         + relativedelta(years=3))

    def test_BD_sub_y(self):
        self.assertEqual(test_date._sub('3y'), comp_date
                         - relativedelta(years=3))

    def test_BD_add_m(self):
        self.assertEqual(test_date._add('3m'), comp_date
                         + relativedelta(months=3))

    def test_BD_sub_m(self):
        self.assertEqual(test_date._sub('3m'), comp_date
                         - relativedelta(months=3))

    def test_BD_add_w(self):
        self.assertEqual(test_date._add('3w'), comp_date
                         + relativedelta(weeks=3))

    def test_BD_sub_w(self):
        self.assertEqual(test_date._sub('3w'), comp_date
                         - relativedelta(weeks=3))

    def test_BD_add_d(self):
        self.assertEqual(test_date._add('3d'), comp_date
                         + relativedelta(days=3))

    def test_BD_sub_d(self):
        self.assertEqual(test_date._sub('3d'), comp_date
                         - relativedelta(days=3))

    def test_num_days(self):
        self.assertEqual(test_date.num_of_days(fut_date), 92)

    def test_date_range(self):
        self.assertEqual([str(date) for date in date_range(
            BankDate(fut_date_range), '3m', test_date)],
            ['2021-10-25', '2021-07-26', '2021-04-26', '2021-01-26', '2020-10-26',
             '2020-07-27', '2020-04-27', '2020-01-27', '2019-10-28', '2019-07-29',
             '2019-04-29', '2019-01-29', '2018-10-29', '2018-07-30', '2018-04-30',
             '2018-01-30', '2017-10-30', '2017-07-31', '2017-05-01', '2017-02-01',
             '2016-11-01', '2016-08-01'])

if __name__ == "__main__":
    from dateutil.relativedelta import relativedelta
    test_date = BankDate('2016-10-24')
    comp_date = datetime.strptime('2016-10-24', '%Y-%m-%d').date()
    fut_date = comp_date + relativedelta(months=3)
    fut_date_range = comp_date + relativedelta(years=5)
    unittest.main()

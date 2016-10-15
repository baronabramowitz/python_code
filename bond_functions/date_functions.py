__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

import bankdate as BD
import strips_data_config as sdc
from datetime import timedelta, datetime


"""Contains the functions related to dates"""


def yields_for_payment_dates(mat_date, pay_step):
    """Generate list of discount rates for coupon payment dates"""
    # Currently hard coded to USD as currency
    days_to_mat_new_dates = days_to_payment(mat_date, pay_step)
    spl = sdc.todays_strips_data_usd
    payment_date_approximate_yields = [
        float(spl(days_to_mat)) for days_to_mat in days_to_mat_new_dates]
    return payment_date_approximate_yields


def yields_for_payment_dates_var(mat_date, pay_step, scenario_spl):
    """Generate list of discount rates for coupon payment dates"""
    # Currently hard coded to USD as currency
    days_to_mat_new_dates = days_to_payment(mat_date, pay_step)
    spl = scenario_spl
    payment_date_approximate_yields = [
        float(spl(days_to_mat)) for days_to_mat in days_to_mat_new_dates]
    return payment_date_approximate_yields


def days_to_payment(mat_date, pay_step):
    '''Return a list of days until coupon dates'''
    new_dates = BD.date_range(mat_date, step='6m')
    days_to_payment = [BD.BankDate().num_of_days(date) for date in new_dates]
    return days_to_payment


if __name__ == "__main__":
    print(yields_for_payment_dates('2022-06-15', '6m'))

"""Contains the functions related to dates"""
__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

import bankdate as BD
import strips_data_config as sdc


def yields_for_payment_dates(payment_dates):
    """Generate list of discount rates for coupon payment dates"""
    # Currently hard coded to USD as currency
    days_to_mat_dates = days_to_payment(payment_dates)
    spl = sdc.todays_strips_data_usd
    payment_date_approximate_yields = [
        float(spl(days_to_mat)) for days_to_mat in days_to_mat_dates]
    return payment_date_approximate_yields


def yields_for_payment_dates_var(payment_dates, scenario_spl):
    """Generate list of discount rates for coupon payment dates"""
    # Currently hard coded to USD as currency

    days_to_mat_dates = days_to_payment(payment_dates)
    payment_date_approximate_yields = [
        float(scenario_spl(days_to_mat)) for days_to_mat in days_to_mat_dates]
    return payment_date_approximate_yields


def days_to_payment(payment_dates):
    """Return a list of days until coupon dates"""

    try:
        days_to_payment = [BD.BankDate().num_of_days(date.bank_date)
                           for date in payment_dates]
        return days_to_payment
    except TypeError:
        return [BD.BankDate().num_of_days(payment_dates.bank_date)]


if __name__ == "__main__":
    print(yields_for_payment_dates('2022-06-15', '6m'))

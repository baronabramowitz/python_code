__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '05/10/2016'

import BankDate_ as BD
import strips_data_config as sdc
from datetime import timedelta, datetime


"""Contains the functions related to dates"""


def payment_dates(dateval, step):
    """Generate the dates on which payments (coupon & principal) occur given maturity date"""
    #Steps in number of months e.g. '6m', '3m', '24m'
    #Default is semi-annual compounding
    new_dates = [ date + '1d' if datetime.weekday(date) == 6 
                else date + '2d' if datetime.weekday(date) == 5 
                else date for date in BD.daterange(dateval, step ='6m')]
    del new_dates[0]
    return(new_dates)


def yields_for_payment_dates(mat_date, pay_step):
    """Generate list of discount rates for coupon payment dates"""
    # Currently hard coded to GBP as currency
    days_to_mat_new_dates = days_to_payment(mat_date, pay_step)
    spl = sdc.todays_strips_data_gbp
    payment_date_approximate_yields = [float(spl(days_to_mat)) for days_to_mat in days_to_mat_new_dates]
    return payment_date_approximate_yields    


def days_to_payment(mat_date, pay_step):
    '''Return a list of days until coupon dates'''
    new_dates = payment_dates(mat_date, pay_step)
    days_to_payment = [BD.BankDate().nbr_of_days(date) for date in new_dates]
    return days_to_payment  


if __name__ == "__main__":
    print(yields_for_payment_dates('2022-06-15', '6m'))  

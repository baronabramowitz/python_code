__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

import BankDate_ as BD
import strips_data_config as sdc
from datetime import timedelta, datetime


"""Contains the functions related to dates"""

def nearest_date(entered_date,todays_strips_data):
    """Return nearest date from list of STRIPS maturity dates."""
    # Currently hard coded to GBP as currency
    # This function works but is certainly very hacky and unelegant. 
    # There must be a better way to perfrom this task than using this dictionary lookup
    dates = sdc.todays_strips_data_gbp['Date'].tolist() #  Input for dates, returned from strips parsing functions
    day_diffs = {}
    for i, date in enumerate(dates):
        day_diffs.update({i:abs(BD.BankDate(date).nbr_of_days(entered_date))})
    return dates[int(min(day_diffs, key=day_diffs.get)) - 1]


def payment_dates(dateval, step):
    '''Generates the dates on which payments (coupon & principal) occur given maturity date

    Steps in number of months e.g. '6m', '3m', '24m'
    Default is semi-annual compounding
    '''

    new_dates = []
    for date in BD.daterange(dateval, step ='6m'):
        if datetime.weekday(date) == 6:
            date = date + '1d'
            new_dates.append(date)
        elif datetime.weekday(date) == 5:
            date = date + '2d'
            new_dates.append(date)
        else:
            new_dates.append(date)
    del new_dates[0]
    return(new_dates)


def yields_for_payment_dates(new_dates):
    """Generates list of discount rates for coupon payment dates

    **Requires the output of strips_data_generation assigned to todays_strips_data 
    to be in memory before this process will function properly**
    """
    # Currently hard coded to GBP as currency
    payment_date_approximate_yields = []
    for date in new_dates:
        payment_date_approximate_yields.append(float((sdc.todays_strips_data_gbp.loc[
            sdc.todays_strips_data_gbp['Date'] == nearest_date(date,sdc.todays_strips_data_gbp)]).iloc[0]['Yield']))
    return payment_date_approximate_yields


def days_to_payment(mat_date, pay_step):
    '''Returns a list of days until coupon dates

    Takes the payment dates outputted from payment_dates 
    and converts them into a day count from the current day (or next business day when appropriate)
    to the date of the respective payment
    '''

    step = pay_step
    dateval = mat_date
    new_dates = payment_dates(dateval, step)
    days_to_payment = []
    for date in new_dates:
        days = BD.BankDate().nbr_of_days(date)
        days_to_payment.append(days)
    return days_to_payment    

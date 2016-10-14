__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

import pandas as pd
import numpy as np
import xlwings as xw
import re
import os
import requests
import quandl
from datetime import date as _pythondate
from datetime import timedelta, datetime
from scipy.interpolate import InterpolatedUnivariateSpline




def strips_data_generation_for_VaR(bond_portfolio_currency):
    """Retrieves STRIPS data from US Treasuries or UK Gilts and generates a VaR scenario of different yield curves.

    Returns a set of interpolated univariate splines of the yields 
    across all available maturity dates for VaR Calculations.
    """
    if bond_portfolio_currency == 'GBP':
        if os.path.isfile('/Users/baronabramowitz/Desktop/strips_data/todays_uk_strips_data_raw' 
                            + str(datetime.now().date())):
            base_data_location_string = ('/Users/baronabramowitz/Desktop/strips_data/todays_uk_strips_data_raw' 
                                        + str(datetime.now().date()))
        else:
            page = requests.get('http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices')
            if page.status_code==200:
                base_data_location_string = ('/Users/baronabramowitz/Desktop/strips_data/todays_uk_strips_data_raw' 
                                            + str(datetime.now().date()))
                raw_xml = open(base_data_location_string,'w')
                raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)
                raw_xml.close()
            else:
                print("link invalid")

        pattern = re.compile("INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE=\"(2\d{3}[-][0-1][0-9][-][0-3][0-9])T.{157}YIELD=\"(\d{1,2}\.\d{12})\"")
        pattern_g1_matches = []
        pattern_g2_matches = []
        for i, line in enumerate(open(base_data_location_string, 'r')): 
            for match in re.finditer(pattern, line):
                pattern_g1_matches.append(match.group(1))
                pattern_g2_matches.append(match.group(2))
        pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
        pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
        strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df,
                                 left_index=True, right_index = True)
        strips_output.columns = ['Date','Yield']
        strips_output['Date'] = pd.to_datetime(strips_output['Date'])
        strips_output = strips_output.sort_values('Date')
        days_to_maturity = [(mat_date - datetime.today()).days for mat_date in strips_output['Date']]
        days_to_mat_series = pd.Series(days_to_maturity)
        strips_output['Days to Maturity'] = days_to_mat_series.values
        strips_output.index = range(0,len(strips_output))
        strips_output = strips_output.drop_duplicates('Date', keep = 'last')
        x1 = strips_output['Days to Maturity']
        y1 = strips_output['Yield']
        spl = InterpolatedUnivariateSpline(x1, y1)
        return (spl, x1)

    elif bond_portfolio_currency == 'USD':
        if os.path.isfile('/Users/baronabramowitz/Desktop/strips_data/todays_us_strips_data_raw' 
                            + str(datetime.now().date())):
            base_data_location_string = '/Users/baronabramowitz/Desktop/strips_data/todays_us_strips_data_raw' + str(datetime.now().date())
        else:
            page = requests.get('http://online.barrons.com/mdc/public/page/9_3020-tstrips.html?mod=bol_topnav_9_3000')
            if page.status_code==200:
                base_data_location_string = '/Users/baronabramowitz/Desktop/strips_data/todays_us_strips_data_raw' + str(datetime.now().date())
                raw_xml = open(base_data_location_string,'w')
                raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)         
                raw_xml.close()
            else:
                print("link invalid")

        pattern_date = re.compile(r"<td class=\"text\">(2[0-9]{3} [a-zA-z]{3} [0-3][0-9])</td>")
        pattern_yield = re.compile(r"<td style=\"border-right:0px\" class=\"num\">([0-9]{1,2}\.[0-9]{2})</td>")
        pattern_g1_matches = []
        pattern_g2_matches = []
        for i, line in enumerate(open(base_data_location_string, 'r')): 
            if i > 2480:
                for match in re.finditer(pattern_date, line):
                    pattern_g1_matches.append(match.group(1))
            else:
                pass

        for i, line in enumerate(open(base_data_location_string, 'r')):
            if i > 2480:
                for match in re.finditer(pattern_yield, line):
                    pattern_g2_matches.append(match.group(1))
            else:
                pass
        
        pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
        pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
        strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df, left_index=True, right_index = True)
        strips_output.columns = ['Date','Yield']
        strips_output['Date'] = pd.to_datetime(strips_output['Date'])
        strips_output = strips_output.sort_values('Date')
        days_to_maturity = [(mat_date - datetime.today()).days for mat_date in strips_output['Date']]
        days_to_mat_series = pd.Series(days_to_maturity)
        strips_output['Days to Maturity'] = days_to_mat_series.values
        strips_output.index = range(0,len(strips_output))
        strips_output = strips_output.drop_duplicates('Date', keep = 'last')
        x1 = strips_output['Days to Maturity']
        y1 = strips_output['Yield']
        spl = InterpolatedUnivariateSpline(x1, y1)
        return (spl, x1)
    else:
        print("Currency not supported")

def var_strips_data_generation(data_start_date, var_days, sample_fraction, currency, ):
    """Generate a set of splines of yield changes for use in VaR calculations
    
    The start date of '1985-12-15' is the first point 
    from which a full 30 year horizon is available

    Some of this code is bound to be circular and will need to be cleaned up
    Performed one iteration of cleaning so far
    """
    print('VaR SDG Start ', datetime.now())
    ustreasury_yield_data = quandl.get("FED/SVENY", authtoken="51d6hxsDAX_CwENkcUEB")
    ustreasury_yield_data.columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    ustreasury_yield_delta = ustreasury_yield_data.diff(var_days)
    ustreasury_yield_delta_modern = ustreasury_yield_delta.ix[data_start_date:str(_pythondate.today())]
    rand_sample = ustreasury_yield_delta_modern.sample(frac=sample_fraction, replace=True)
    for i in range(31, 41):
        rand_sample[i] = rand_sample[30]
    rand_sample[0] = rand_sample[1]
    rand_sample.sort_index(axis=1, inplace=True)
    xrange = range(0,41)
    mat_dates = strips_data_generation_for_VaR(currency)[1]
    spl_list = [InterpolatedUnivariateSpline(xrange, row[1:]) for row in rand_sample.itertuples()]
    years_for_payments = [days/365 for days in  mat_dates]
    yield_change_list = [[spl(years) for years in years_for_payments] for spl in spl_list]
    base_yield_curve = strips_data_generation_for_VaR(currency)[0]
    base_yield_points = [base_yield_curve(mat_date) for mat_date in mat_dates]
    yield_scenario_set = [[y1 + y2 for y1,y2 in zip(yield_delta_set, base_yield_points)] for yield_delta_set in yield_change_list]
    final_spl_set = [ InterpolatedUnivariateSpline(mat_dates, y_set)for y_set in yield_scenario_set]
    print('VaR SDG End   ', datetime.now())
    return final_spl_set

if __name__ == "__main__":
    var_strips_data_generation(10, .1, 'USD', '1985-12-15')




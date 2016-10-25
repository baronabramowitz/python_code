__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

import os
import re
from datetime import datetime

import pandas as pd
import requests
from scipy.interpolate import InterpolatedUnivariateSpline


def strips_data_generation(bond_portfolio_currency):
    """Retrieves STRIPS data from US Treasuries or UK Gilts.

    Returns a interpolated univarite spline of the yields across all available maturity dates.

    Given access to more frequent data then prior trading day end,
    will update to use interday updated strips data.
    This should be a much quicker process since the get from a dedicated
    data source will be faster than regex parsing the
    raw html data.
    A proper HF data source will likely return XML or JSON formatted
    responses which can be unpacked via several different python libraries
    and remove the need for the regex below.
    The process would ideally be run outside the critical path and the
    resulting data referenced from within the function itself.

    Ideally would add some code that would input a bond portfolio containing both
    GBP and USD bonds and split them into two portfolios of the respective currency
    and then apply the below yield curves.

    Eventually will add more functionality to accept other currencies 
    and the ability to differentiate between location of government issue
    for Eurozone countries.
    """
    if bond_portfolio_currency == 'GBP':
        if os.path.isfile('/Users/baronabramowitz/Desktop/strips_data/todays_uk_strips_data_raw'
                          + str(datetime.now().date())):
            base_data_location_string = ('/Users/baronabramowitz/Desktop/strips_data/todays_uk_strips_data_raw'
                                         + str(datetime.now().date()))
        else:
            page = requests.get(
                'http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices')
            if page.status_code == 200:
                base_data_location_string = ('/Users/baronabramowitz/Desktop/strips_data/todays_uk_strips_data_raw'
                                             + str(datetime.now().date()))
                raw_xml = open(base_data_location_string, 'w')
                raw_xml.write('Download Timestamp: ' +
                              str(datetime.now()) + page.text)
                raw_xml.close()
            else:
                print("link invalid")

        pattern = re.compile(
            r"INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE=\"(2\d{3}[-][0-1][0-9][-][0-3][0-9])T.{157}YIELD=\"(\d{1,2}\.\d{12})\"")
        pattern_g1_matches = []
        pattern_g2_matches = []
        for i, line in enumerate(open(base_data_location_string, 'r')):
            for match in re.finditer(pattern, line):
                pattern_g1_matches.append(match.group(1))
                pattern_g2_matches.append(match.group(2))
        pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
        pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
        strips_output = pd.merge(pattern_g1_matches_df, pattern_g2_matches_df,
                                 left_index=True, right_index=True)
        strips_output.columns = ['Date', 'Yield']
        strips_output['Date'] = pd.to_datetime(strips_output['Date'])
        strips_output = strips_output.sort_values('Date')
        days_to_maturity = [
            (mat_date - datetime.today()).days for mat_date in strips_output['Date']]
        days_to_mat_series = pd.Series(days_to_maturity)
        strips_output['Days to Maturity'] = days_to_mat_series.values
        strips_output.index = range(0, len(strips_output))
        strips_output = strips_output.drop_duplicates('Date', keep='last')
        x1 = strips_output['Days to Maturity']
        y1 = strips_output['Yield']
        spl = InterpolatedUnivariateSpline(x1, y1)
        return spl

    elif bond_portfolio_currency == 'USD':
        if os.path.isfile('/Users/baronabramowitz/Desktop/strips_data/todays_us_strips_data_raw'
                          + str(datetime.now().date())):
            base_data_location_string = '/Users/baronabramowitz/Desktop/strips_data/todays_us_strips_data_raw' + \
                str(datetime.now().date())
        else:
            page = requests.get(
                'http://online.barrons.com/mdc/public/page/9_3020-tstrips.html?mod=bol_topnav_9_3000')
            if page.status_code == 200:
                base_data_location_string = '/Users/baronabramowitz/Desktop/strips_data/todays_us_strips_data_raw' + \
                    str(datetime.now().date())
                raw_xml = open(base_data_location_string, 'w')
                raw_xml.write('Download Timestamp: ' +
                              str(datetime.now()) + page.text)
                raw_xml.close()
            else:
                print("link invalid")

        pattern_date = re.compile(
            r"<td class=\"text\">(2[0-9]{3} [a-zA-z]{3} [0-3][0-9])</td>")
        pattern_yield = re.compile(
            r"<td style=\"border-right:0px\" class=\"num\">([0-9]{1,2}\.[0-9]{2})</td>")
        pattern_g1_matches = []
        pattern_g2_matches = []
        for i, line in enumerate(open(base_data_location_string, 'r')):
            if i > 2407:
                for match in re.finditer(pattern_date, line):
                    pattern_g1_matches.append(match.group(1))
            else:
                pass

        for i, line in enumerate(open(base_data_location_string, 'r')):
            if i > 2407:
                for match in re.finditer(pattern_yield, line):
                    pattern_g2_matches.append(match.group(1))
            else:
                pass

        pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
        pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
        strips_output = pd.merge(
            pattern_g1_matches_df, pattern_g2_matches_df, left_index=True, right_index=True)
        strips_output.columns = ['Date', 'Yield']
        strips_output['Date'] = pd.to_datetime(strips_output['Date'])
        strips_output = strips_output.sort_values('Date')
        days_to_maturity = [
            (mat_date - datetime.today()).days for mat_date in strips_output['Date']]
        days_to_mat_series = pd.Series(days_to_maturity)
        strips_output['Days to Maturity'] = days_to_mat_series.values
        strips_output.index = range(0, len(strips_output))
        strips_output = strips_output.drop_duplicates('Date', keep='last')
        x1 = strips_output['Days to Maturity']
        y1 = strips_output['Yield']
        spl = InterpolatedUnivariateSpline(x1, y1)
        return spl
    else:
        print("Currency not supported")

if __name__ == "__main__":
    strips_data_generation('USD')

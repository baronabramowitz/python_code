__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '22/08/2016'

"""Bond VaR Code & Bond Portfolio VaR Code
This is currently not functional, work in progress
"""

import pandas as pd
from math import sqrt


def generate_yield_comparison_table_raw(csv_location):
    """Builds a table containing daily yield quotes of corporate bonds

    Function works as intended but the CSV could be updted outside of 
    the critical path each day to refelct the added observation to the 
    historic yield changes, need to figure out how to tie the historic
    spot rate changes over comparable horizons to each rate in the strips data
    And then revaluing the bond under these new yields
    """

    daily_yield_change_array = pd.read_csv(csv_location,
                                           header = 0,
                                           delimiter = ',',
                                           converters = {'Date':str,'2yr AA':np.float64,'2yr A':np.float64,
                                                        '5yr AAA':np.float64,'5yr AA':np.float64, '5yr A':np.float64,
                                                        '10yr AAA':np.float64, '10yr AA':np.float64,'10yr A':np.float64,
                                                         '20yr AAA':np.float64,'20yr AA':np.float64, '20yr A':np.float64,
                                            }
    )
    return daily_yield_change_array


yesterdays_yield_close_values_corp = generate_yield_comparison_table_raw (
    '/Users/baronabramowitz/Desktop/corporate_bond_yields_daily_values.csv').iloc[[0]] 


def value_at_risk_yield_change_upper_bound_by_rating(csv_location,loss_percentile):
    """Takes a table of daily bond yield quotes, extracts the quotes for the ratings, determines the lower bound for the inputted percentile.

    Currently supported bond ratings limited to:                    
                        'Corporate 2yr AA','Corporate 2yr A',
    'Corporate 5yr AAA','Corporate 5yr AA', 'Corporate 5yr A',
    'Corporate 10yr AAA','Corporate 10yr AA','Corporate 10yr A', 
    'Corporate 20yr AAA','Corporate 20yr AA', 'Corporate 20yr A'
    Percentile as a whole number, eg 95th percentile as 95 not .95.
    Intended to be run before trading, once a trading day and the VaR bounds should be stored.
    """

    daily_yield_change_array = generate_yield_comparison_table_raw(csv_location)
    upper_bounds = []
    bond_ratings_set = ['2yr_AA','2yr_A',
                        '5yr_AAA','5yr_AA', '5yr_A',
                        '10yr_AAA','10yr_AA','10yr_A',
                        '20yr_AAA','20yr_AA', '20yr_A'
    ]
    for bond_rating_val in bond_ratings_set:
        upper_bounds.append(np.percentile(daily_yield_change_array[bond_rating_val],loss_percentile))

    upper_bound_set = dict(zip(bond_ratings_set,upper_bounds))
    return upper_bound_set


def value_at_risk_single_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type,csv_location,loss_percentile):
    """ Calculates the Value at Risk for a single bond.

    Needs to be updated to reflect the new method of calculating discount rates 
    which is not based on bond maturity/rating but rather a rating premium on 
    top of the risk free strips yield curve"""

    val_bond_output = value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type)
    discount_rate = sum(val_bond_output[4])/len(val_bond_output[4])
    upper_bound = value_at_risk_yield_change_upper_bound_by_rating(csv_location,loss_percentile)[bond_rating]
    new_discount_rate = discount_rate + upper_bound
    new_bond_val = value_bond_var(face_value,maturity_date,coupon_rate,payments_per_year,new_discount_rate)[0]
    v_a_r_single_bond = val_bond_output[0] - new_bond_val
    v_a_r_single_bond_percent = v_a_r_single_bond * 100 / val_bond_output[0]
    return {'VaR' : v_a_r_single_bond, 'VaR Percentage' : v_a_r_single_bond_percent}

yield_change_matrix = generate_yield_comparison_table_raw (
            '/Users/baronabramowitz/Desktop/cleaned_corporate_bond_yield_change_data.csv')
yield_change_corr_matrix = yield_change_matrix.corr()
yield_change_cov_matrix = yield_change_matrix.cov()


def value_at_risk_portfolio_set(portfolio_csv_location,loss_percentile):
    """Calculates the Value at Risk for an entire portfolio

    the value_at_risk_single_bond needs to be updated before this can function properly
    """
    portfolio = generate_portfolio(portfolio_csv_location)
    val_portfolio_output = value_portfolio(portfolio_csv_location)

    loss_percentiles_pre_zip = []
    for item in val_portfolio_output['Set of Bond Values']:
        loss_percentiles_pre_zip.append(loss_percentile)

    yield_change_csv_location_pre_zip = []
    for item in val_portfolio_output['Set of Bond Values']:
        yield_change_csv_location_pre_zip.append(
            '/Users/baronabramowitz/Desktop/cleaned_corporate_bond_yield_change_data.csv')

    bond_var_portfolio_squared = []
    for bond in zip(portfolio['face_value'],portfolio['maturity_date'],portfolio['coupon_rate'],
                   portfolio['payments_per_year'],portfolio['bond_rating'],portfolio['bond_type'],
                   yield_change_csv_location_pre_zip,loss_percentiles_pre_zip
                   ):
        bond_var = value_at_risk_single_bond(*bond)['VaR']
        bond_var_squared = bond_var ** 2
        bond_var_portfolio_squared.append(bond_var_squared)

    inter_sum_bond_var_squared = sum(bond_var_portfolio_squared)
    portfolio_value_at_risk = sqrt(inter_sum_bond_var_squared)
    portfolio_value_at_risk_percent = (portfolio_value_at_risk * 100 
                                    / val_portfolio_output['Portfolio Value'])
    return {'Portfolio VaR' : portfolio_value_at_risk, 
            'Portfolio VaR Percent' : portfolio_value_at_risk_percent 
            }
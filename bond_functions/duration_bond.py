__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

"""Bond Duration Code & Bond Portfolio Duration Code"""

import value_bond as vb
import generate_portfolio as gp


def duration_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type):
    """Calculates the duration and Macaulay/Modified duration"""

    value_bond_output_db = vb.value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type)
    intermediate_dur_calcs = []
    years_to_payments = [days / 365 for days in value_bond_output_db[2]]

    for cf in zip(value_bond_output_db[1],years_to_payments):
        intermediate_dur_calcs.append(cf[0] * cf[1])
        
    bond_duration = sum(intermediate_dur_calcs)/value_bond_output_db[0]
    mm_duration = bond_duration/(1 + sum(value_bond_output_db[4])/len(value_bond_output_db[4]) / 100)
    return {'Bond Duration' : bond_duration, 'Modified Duration' : mm_duration}


def duration_portfolio(csv_location):
    """Calculates the duration and Macaulay/Modified duration of a portfolio of bonds"""

    bond_dur_portfolio=[]
    mm_bond_dur_portfolio=[]
    weighted_bond_dur_portfolio = []
    weighted_mm_bond_dur_portfolio = []
    portfolio = gp.generate_portfolio(csv_location)
    val_portfolio_output = vb.value_portfolio(csv_location)

    for bond in zip(portfolio['face_value'],portfolio['maturity_date'],portfolio['coupon_rate'],
                   portfolio['payments_per_year'],portfolio['bond_rating'],portfolio['bond_type']
                   ):
        bond_dur = duration_bond(*bond)['Bond Duration']
        bond_dur_portfolio.append(bond_dur)
        mm_bond_dur = duration_bond(*bond)['Modified Duration']
        mm_bond_dur_portfolio.append(mm_bond_dur)

    for group in list(zip(bond_dur_portfolio,val_portfolio_output['Set of Bond Values'],mm_bond_dur_portfolio)):
        scale_bond_dur_by_portfolio_value = group[0]*group[1]/val_portfolio_output['Portfolio Value']
        weighted_bond_dur_portfolio.append(scale_bond_dur_by_portfolio_value)
        scale_mm_bond_dur_by_portfolio_value = group[2]*group[1]/val_portfolio_output['Portfolio Value']
        weighted_mm_bond_dur_portfolio.append(scale_mm_bond_dur_by_portfolio_value)

    portfolio_dur = sum(weighted_bond_dur_portfolio)
    mm_portfolio_dur = sum(weighted_mm_bond_dur_portfolio)
    return {'Portfolio Duration' : portfolio_dur, 'Modified Portfolio Duration' : mm_portfolio_dur}

if __name__ == "__main__":
	#print(duration_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
    print(duration_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))




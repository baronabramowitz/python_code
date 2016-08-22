__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

"""Bond Convexity Code & Bond Portfolio Convexity Code"""
import value_bond as vb
import generate_portfolio as gp


def convexity_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type):
    """Calculates the convexity of an indivudal bond"""

    value_bond_output_cb = vb.value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type)
    intermediate_conv_calcs = []
    years_to_payments = [(days / 365) for days in value_bond_output_cb[2]]
    cfs = list(zip(value_bond_output_cb[1],years_to_payments))

    for pv_cf in cfs:
        inter_conv_calc =  (pv_cf[0])*(pv_cf[1]**2+pv_cf[1])
        intermediate_conv_calcs.append(inter_conv_calc)
        
    bond_convexity = (sum(intermediate_conv_calcs) 
                    / (value_bond_output_cb [0] 
                    * (1 + sum(value_bond_output_cb[4])/len(value_bond_output_cb[4]) / 100)**2))
    return {'Bond Convexity':bond_convexity}


def convexity_portfolio(csv_location):
    """Calcualtes the convexity of a portfolio of bonds"""

    bond_conv_portfolio = []
    weighted_bond_conv_portfolio = []
    portfolio = gp.generate_portfolio(csv_location)
    val_portfolio_output = vb.value_portfolio(csv_location)

    for bond in zip(portfolio['face_value'],portfolio['maturity_date'],portfolio['coupon_rate'],
                   portfolio['payments_per_year'],portfolio['bond_rating'],portfolio['bond_type']
                ):
        bond_conv = convexity_bond(*bond)['Bond Convexity']
        bond_conv_portfolio.append(bond_conv)

    for entry in zip(bond_conv_portfolio,val_portfolio_output['Set of Bond Values']):
        scale_bond_conv_by_portfolio_value = entry[0]*entry[1]/val_portfolio_output['Portfolio Value']
        weighted_bond_conv_portfolio.append(scale_bond_conv_by_portfolio_value)

    portfolio_convexity = sum(weighted_bond_conv_portfolio)
    return {'Portfolio Convexity':portfolio_convexity}

if __name__ == "__main__":
	#print(convexity_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
    print(convexity_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
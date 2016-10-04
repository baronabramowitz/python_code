__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '23/09/2016'

"""Bond Valuation Code & Bond Portfolio Valuation Code"""
import date_functions as df
import generate_portfolio as gp
import strips_data_generation as sdg
import BankDate_ as BD


def value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type):
    """Values bond given current inputs."""

    pv_fcf = []
    payment_step = str(payments_per_year/12) + 'm'
    discount_rates = df.yields_for_payment_dates(df.payment_dates(maturity_date, payment_step))
    days_to_payments = df.days_to_payment(maturity_date,payment_step)

    # Currently bond premiums are hard coded but a more scalable version
    # would include these premiums being stored elsewhere and referenced 
    # within the function; this would allow for distributing the bond valuations
    # across multiple processors when valuing a portfolio.
    # These premiums stored elsewhere could be periodically updated whilst remaining out of the critical path

    if bond_type == 'Corporate':
        if bond_rating == 'AAA':
            rating_premium = .015
        elif bond_rating == 'AA':
            rating_premium = .025
        elif bond_rating == 'A':
            rating_premium = .035
        else:
            pass
    elif bond_type == 'Government':
        if bond_rating == 'AAA':
            rating_premium = 0
        elif bond_rating == 'AA':
            rating_premium = .015
        elif bond_rating == 'A':
            rating_premium = .025
        else:
            pass
    else:
        pass

    discount_rates = [x * (1 + rating_premium) for x in discount_rates]

    bond_maturity_remaining = (BD.BankDate().nbr_of_days(maturity_date))/365

    if payments_per_year == 0:
        coupon_payment = 0
    else:
        coupon_payment = ((coupon_rate/100)*face_value)/payments_per_year

    for i, day_count in enumerate(days_to_payments):
        if day_count == max(days_to_payments):
            pv_cf = (coupon_payment + face_value)/((1+(discount_rates[i]/100/365))**day_count)
            pv_fcf.append(pv_cf)
        elif day_count != 0 and day_count != max(days_to_payments):
            pv_cf = coupon_payment/((1+(discount_rates[i]/100/365))**day_count)
            pv_fcf.append(pv_cf)
        else:
            pass

    bond_val = sum(pv_fcf)
    return (bond_val, pv_fcf, days_to_payments, bond_maturity_remaining, discount_rates)


def value_bond_VaR(face_value,maturity_date,coupon_rate,payments_per_year,discount_rate):
    """Values bond for value at risk function"""

    pv_fcf = []
    bond_maturity_remaining = (BD.BankDate().nbr_of_days(maturity_date))/365
    payment_step = str(payments_per_year/12) + 'm'
    if payments_per_year == 0:
        coupon_payment = 0
    else:
        coupon_payment = ((coupon_rate/100)*face_value)/payments_per_year
    days_to_payments = df.days_to_payment(maturity_date,payment_step)

    for day_count in days_to_payments:
        if day_count == max(days_to_payments):
            pv_cf = (coupon_payment + face_value)/((1+(discount_rate/100/365))**day_count)
            pv_fcf.append(pv_cf)
        elif day_count != 0 and day_count != max(days_to_payments):
            pv_cf = coupon_payment/((1 + (discount_rate/100/365))**day_count)
            pv_fcf.append(pv_cf)
        else:
            pass

    bond_val = sum(pv_fcf)
    return (bond_val, pv_fcf, days_to_payments, bond_maturity_remaining, discount_rate)


def value_portfolio(csv_location):
    """Calculates the value of a portfolio of bonds (as a CSV)"""
    portfolio = gp.generate_portfolio(csv_location)
    bond_val_portfolio = [(value_bond(*bond)[3]) for bond in zip(portfolio['face_value'],portfolio['maturity_date'],
        portfolio['coupon_rate'],portfolio['payments_per_year'],portfolio['bond_rating'],portfolio['bond_type'])]
    bond_maturity_set = [(value_bond(*bond)[0]) for bond in zip(portfolio['face_value'],portfolio['maturity_date'],
        portfolio['coupon_rate'],portfolio['payments_per_year'],portfolio['bond_rating'],portfolio['bond_type'])]
    portfolio_val = sum(bond_val_portfolio)
    return {'Portfolio Value':portfolio_val, 'Set of Bond Values' : bond_val_portfolio, 'Set of Bond Maturities' : bond_maturity_set}



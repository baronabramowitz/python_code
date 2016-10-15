__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '15/10/2016'

"""Portfolio Generation Code"""

import bond_class as bc
import var_scenario_gen as vsg
import decimal
from datetime import datetime, timedelta

import babel.numbers
import numpy as np
import pandas as pd
import psycopg2


def generate_portfolio(csv_location):
    """Generate portfolio list of Bond objects from the CSV at the inputted location

        Still functional but no longer used as SQL below scales better
        """

    portfolio = pd.read_csv(csv_location,
                            header=0,
                            delimiter=',',
                            converters={'face_value': np.float64, 'maturity_date': str, 'coupon_rate': np.float64,
                                        'payments_per_year': np.float64, 'rating': str, 'btype': str})
    for row in portfolio.itertuples():
        print(row[1:])
    portfolio = [bc.Bond(*row[1:]) for row in portfolio.itertuples()]
    return portfolio


def generate_portfolio_psql(bond_set):
    """Generate portfolio from bond set in DB"""

    try:
        conn = psycopg2.connect(
            "dbname='fi_data' user='pyconnect' host='localhost' password='pypwcon'")
    except:
        print("I am unable to connect to the database")
    conn = psycopg2.connect(
        "dbname='fi_data' user='pyconnect' host='localhost' password='pypwcon'")
    cur = conn.cursor()
    if bond_set == 'All':
        cur.execute("SELECT * FROM bond_data")
    elif bond_set == 'Corporate':
        cur.execute(
            "SELECT * FROM bond_data WHERE bond_json ->> 'type' = 'Corporate'")
    elif bond_set == 'Government':
        cur.execute(
            "SELECT * FROM bond_data WHERE bond_json ->> 'type' = 'Government'")
    else:
        print('What you doing mate?')
    portfolio = [bc.Bond(*tuple((d[1]['face_value'], d[1]['maturity_date'], d[1]['coupon_rate'],
                                 d[1]['payments_per_year'], d[1]['rating'], d[1]['type']))) for d in cur.fetchall()]
    cur.close()
    conn.close()
    return portfolio


class Portfolio(object):
    """A portfolio class that contains a set of Bond objects"""

    def __init__(self, bond_set, currency):
        # self.contents = generate_portfolio(csv_location)
        self.contents = generate_portfolio_psql(bond_set)
        self.currency = currency

    def value(self):
        """Generate the value the portfolio"""
        return sum([bond.value() for bond in self.contents])

    def value_formatted(self):
        """Generate the value the portfolio formatted with the respective currency"""
        return babel.numbers.format_currency(decimal.Decimal(str(
            sum([bond.value() for bond in self.contents]))), self.currency)

    def value_var(self, scenario_spl):
        """Generate the value the portfolio"""
        return sum([bond.value_var(scenario_spl) for bond in self.contents])

    def contents_value(self):
        """Generate the value of each bond in the portfolio"""
        return [bond.value() for bond in self.contents]

    def contents_maturity(self):
        """Generate the maturity in years of each bond in the portfolio"""
        return [bond.maturity_remaining() for bond in self.contents]

    def duration(self):
        """Generate the duration the portfolio"""
        return sum([(bond.duration() * bond.value()) / self.value() for bond in self.contents])

    def contents_duration(self):
        """Generate the duration contribution of each bond in the portfolio"""
        return [(bond.duration() * bond.value()) / self.value() for bond in self.contents]

    def modified_duration(self):
        """Generate the modified duration the portfolio"""
        return sum([(bond.modified_duration() * bond.value()) / self.value() for bond in self.contents])

    def contents_modified_duration(self):
        """Generate the modified duration contribution of each bond in the portfolio"""
        return [(bond.modified_duration() * bond.value()) / self.value() for bond in self.contents]

    def convexity(self):
        """Generate the convexity the portfolio"""
        return sum([(bond.convexity() * bond.value()) / self.value() for bond in self.contents])

    def contents_convexity(self):
        """Generate the convexity contribution of each bond in the portfolio"""
        return [(bond.convexity() * bond.value()) / self.value() for bond in self.contents]

    def value_at_risk(self, data_start_date, var_day_count, var_subsample_fraction, var_percentile):
        """Generate the Value at Risk for the portfolio

        Uses a subset of historical yield curve shifts (can use all of them) to model possible
        yield curve movements. Return the percentile specified of the set of loss scenarios as
        both a formatted value and a percentage of portfolio value.

        *Currently Biggest Issue*
        The function recalculates the days to each payment for each bond every time it values the bond;
        Long term solution, rewrite so that days to payment for each bond only calc'd once per bond and
        then passed to the appropriate functions
        Short term solution, rewrote the pv fcf method to only calc dtp once per bond valuation, not 3
        times; I am an idiot, this cut runtime by 89%
        """
        # print(datetime.now(), 'Starting scenario evaluations.')
        var_strips_data = vsg.var_strips_data_generation(
            data_start_date, var_day_count, var_subsample_fraction, self.currency)
        VaR_value_set = np.array([self.value_var(scenario_spl)
                                  for scenario_spl in var_strips_data])
        portfolio_value_bottom = np.percentile(
            VaR_value_set, (1 - (var_percentile / 100)))
        VaR = self.value() - portfolio_value_bottom
        VaR_formatted = babel.numbers.format_currency(
            decimal.Decimal(str(VaR)), self.currency)
        VaR_percentile = str((VaR / self.value()) * 100) + '%'
        return {'VaR': VaR_formatted, 'VaR Percentage': VaR_percentile}


if __name__ == "__main__":
    portfolio_test = Portfolio('All', 'USD')
    print(portfolio_test.value_at_risk('1985-12-25', 1, 1, 95))

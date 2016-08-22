__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

"""Portfolio Generation Code"""

import pandas as pd
import numpy as np

def generate_portfolio(csv_location):
    """Generates portfolio DataFrame from the CSV at the inputted location"""

    portfolio = pd.read_csv(csv_location,
                           header = 0,
                           delimiter = ',',
                           converters = {'face_value':np.float64,'maturity_date':str,'coupon_rate':np.float64,
                                         'payments_per_year':np.float64,'bond_rating':str,'bond_type':str
                            }
    )
    return portfolio


__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '21/08/2016'

"""Set up global STRIPS data"""

import strips_data_generation as sdg

todays_strips_data_usd = sdg.strips_data_generation('USD')
todays_strips_data_gbp = sdg.strips_data_generation('GBP')


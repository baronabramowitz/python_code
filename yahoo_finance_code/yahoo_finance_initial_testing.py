__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '23/08/2016'

import yahoo_finance
from yahoo_finance import Share
#from yahoo_finance import Currency
from pprint import pprint


gbp_usd = Currency('GBPUSD')

print(gbp_usd.get_rate())
#print(gbp_usd.refresh()) if this line is not ommitted, 
# the rate seldom ends up between the bid and the ask
print(gbp_usd.get_bid())
print(gbp_usd.get_ask())

disney = Share('DIS')

pprint(disney.get_avg_daily_volume()) #'7230930'
pprint(disney.get_price()) #'95.98'
pprint(disney.get_change()) #'+0.11'
pprint(disney.get_volume()) #'2533504'
pprint(disney.get_prev_close()) #'95.87'
pprint(disney.get_open()) #'96.13'
pprint(disney.get_stock_exchange()) #'NYQ'
pprint(disney.get_market_cap()) #'154.25B'
pprint(disney.get_book_value()) #'26.00'
pprint(disney.get_ebitda()) #'17.15B'
pprint(disney.get_dividend_share()) #'1.42'
pprint(disney.get_dividend_yield()) #'1.47'
pprint(disney.get_earnings_share()) # '5.56'
pprint(disney.get_days_high()) #'96.43'
pprint(disney.get_days_low()) #'95.87'
pprint(disney.get_year_high()) #'120.65'
pprint(disney.get_year_low()) #'86.25'
pprint(disney.get_50day_moving_avg()) #'97.49'
pprint(disney.get_200day_moving_avg()) #'98.35'

#pprint(disney.get_price_earnings_ratio()) #'17.25'

#print(float(disney.get_price())/float(disney.get_earnings_share()))

pprint(disney.get_price_earnings_growth_ratio()) #'1.55'
pprint(disney.get_price_sales()) #'2.75'
pprint(disney.get_price_book()) #'3.69'
pprint(disney.get_short_ratio()) #'5.92'
pprint(disney.get_trade_datetime()) #'2016-08-23 16:25:00 UTC+0000'
pprint(disney.get_info()) #{'symbol': 'DIS'}
#pprint(disney.get_historical('2008-08-22', '2016-08-22'))

"""{'Adj_Close': '95.870003',
  'Close': '95.870003',
  'Date': '2016-08-22',
  'High': '96.470001',
  'Low': '95.650002',
  'Open': '96.470001',
  'Symbol': 'DIS',
  'Volume': '5481700'}
  For each trading day between end date and start date in a list
  """


__version__ = '0.1.0'
__author__ = 'Baron Abramowitz'

from datetime import date as _pythondate
from datetime import timedelta, datetime
import re
from math import sqrt
import pandas as pd
import numpy as np
import requests

from abc import ABCMeta, abstractmethod
import unittest
import xlwings as xw


"""
Code to line 511 was taken from another depository.
Most of it is unused, will go back and clean up unused portions eventually.
Will change function outputs from dictionaries to named tuples
"""
class CummutativeAddition:
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def __neg__(self):
        raise NotImplementedError

    @abstractmethod
    def __abs__(self):
        raise NotImplementedError

    @abstractmethod
    def __add__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __rsub__(self, other_value):
        '''__rsub__ has to be defined to handle right side subtraction since
        subtraction otherwise is specified at the left value.
        '''
        raise NotImplementedError

    def __radd__(self, other_value):
        return  self.__add__(other_value)

    def __sub__(self, other_value):
        return self.__add__(-other_value)

    def __iadd__(self, other_value):
        return  self.__add__(other_value)

    def __isub__(self, other_value):
        return self.__add__(-other_value)


class CummutativeMultiplication:
    

    __metaclass__ = ABCMeta

    @abstractmethod
    def __mul__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __div__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __rdiv__(self, other_value):
        raise NotImplementedError

    def __rmul__(self, other_value):
        return self.__mul__(other_value)


class Power:
    

    __metaclass__ = ABCMeta

    @abstractmethod
    def __pow__(self, other_value):
        raise NotImplementedError

    @abstractmethod
    def __rpow__(self, other_value):
        raise NotImplementedError

    def __ipow__(self, other_value):
        return self.__pow__(other_value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()


class BankDateError(Exception):
    '''A class to implement error messages from class BankDate.'''
    pass


class TimePeriod(CummutativeAddition, CummutativeMultiplication):
    
    def __init__(self, period):
        
        self._count = None
        self._unit = None
        if isinstance(period,  TimePeriod):
            self._count = period.count
            self._unit = period.unit
        elif isinstance(period,  str):
            validate_period_ok = re.search('^(-?\d*)([d|w|m|y])$', period)
            if validate_period_ok:
                self._count, self._unit = validate_period_ok.groups()
                self._count = int(self._count)

    def __nonzero__(self):
        return 0 if self._count == None else 1

    def __str__(self):
        
        return '%s%s' % (self._count,  self._unit)

    __repr__ = __str__

    def __abs__(self):
        result = self.__class__(self)
        result.count = abs(result.count)
        return result

    def __neg__(self):
        result = self.__class__(self)
        result.count = -result.count
        return result

    def __add__(self, added_value):
       
        result = self.__class__(self)
        if isinstance(added_value, int):
            result.count += added_value
            return result
        if isinstance(added_value, TimePeriod):
            result.count += added_value.count
            return result

    def __rsub__(self, added_value):
        
        return self.__add__(- added_value)

    def __mul__(self, value):
        if isinstance(value, int):
            result = self.__class__(self)
            result.count *= value
            return result

    def __div__(self, value):
        
        if isinstance(value, int):
            result = self.__class__.__init__(self)
            result.count *= value
            return result

    def __rdiv__(self, other_value):
        return

    def __cmp__(self, period):
     
        if isinstance(period,  TimePeriod):
            if self.unit == period.unit:
                if self.count == period.count:
                    return 0
                elif self.count < period.count:
                    return -1
                elif self.count > period.count:
                    return 1
            else:
                raise BankDateError(
                'Non comparable units (%s) vs (%s)'
                % (self.unit,  period.unit))
        else:
            raise BankDateError(
            'Can not compare a TimePeriod with %s of type %s'
            % (period,  type(period)))

    def _get_count(self):
        
        return self._count

    def _set_count(self, value):
        '''set value of poperty count, type integer.'''
        if isinstance(value, int):
            self._count = value
        else:
            raise BankDateError('Value must be an integer, not (%s) of type %s'
                                    % (value,  type(value)))

    count = property(_get_count, _set_count)

    def _get_unit(self):
        '''Unit part [y(ears), m(onths) or d(ays)] of TimePeriod.
        '''
        return self._unit

    unit = property(_get_unit)


class BankDate(_pythondate):

    def __new__(self, bank_date=_pythondate.today()):
        day = None
        if isinstance(bank_date, str):
            try:
                day = datetime.strptime(bank_date, "%Y-%m-%d").date()
            except:
                pass
        elif isinstance(bank_date, _pythondate):
            day = bank_date
        elif isinstance(bank_date, BankDate):
            day = bank_date.date()
        if day:
            return super(BankDate, self).__new__(self,
                                                 day.year,
                                                 day.month,
                                                 day.day
                                                 )
        else:
            return None

    def __str__(self):
        return '%4d-%02d-%02d' % (self.year, self.month, self.day)

    __repr__ = __str__

    def __add__(self, period):
        '''A TimePeriod can be added to a BankDate
        '''
        period = TimePeriod(period)
        if period:
            if period.unit == 'y':
                return self.__class__(self).add_years(period.count)
            elif period.unit == 'm':
                return self.__class__(self).add_months(period.count)
            elif period.unit == 'w':
                return self.__class__(self).add_days(7 * period.count)
            elif period.unit == 'd':
                return self.__class__(self).add_days(period.count)

    def __radd__(self, period):
        '''A BankDate can be added to a TimePeriod
        '''
        return self.__add__(period)

    def __iadd__(self, period):
        '''A TimePeriod can be added to a BankDate
        '''
        return self.__add__(period)

    def __sub__(self, value):
        '''A BankDate can be subtracted either a TimePeriod or a BankDate
        giving a BankDate or the number of days between the 2 BankDates
        '''
        period = TimePeriod(value)
        if period:
            return self.__class__(self).__add__(-period)
        else:
            return -self.nbr_of_days(value)

    def __rsub__(self, date):
        '''A TimePeriod or a BankDate can be subtracted a BankDate giving a
        BankDate or the number of days between the 2 BankDates
        '''
        return self.__sub__(date)

    @staticmethod
    def ultimo(nbr_month):
        '''Return last day of month for a given number of month.

        :param nbr_month: Number of month
        :type nbr_month: int
        '''
        if isinstance(nbr_month, int):
            ultimo_month = {2: 28, 4: 30, 6: 30, 9: 30, 11: 30}
            if nbr_month in ultimo_month:
                return ultimo_month[nbr_month]
            else:
                return 31

    def is_ultimo(self):
        '''Identifies if BankDate is ultimo'''
        return BankDate.ultimo(self.month) == self.day

    def add_months(self, nbr_months):
        '''Adds nbr_months months to the BankDate.

        :param nbr_months: Number of months to be added
        :type nbr_months: int
        '''
        if isinstance(nbr_months, int):
            totalmonths = self.month + nbr_months
            year = self.year + totalmonths // 12
            if not totalmonths % 12:
                year -= 1
            month = totalmonths % 12 or 12
            day = min(self.day, BankDate.ultimo(month))
            return BankDate(_pythondate(year, month, day))

    def add_years(self, nbr_years):
        '''Adds nbr_years years to the BankDate.

        :param nbr_years: Number of years to be added
        :type nbr_years: int

         '''
        if isinstance(nbr_years, int):
            result = _pythondate(self.year + nbr_years, self.month, self.day)
            return BankDate(result)

    def add_days(self, nbr_days):
        '''Adds nbr_days days to the BankDate.

        :param nbr_days: Number of days to be added
        :type nbr_days: int
         '''
        if isinstance(nbr_days, int):
            result = _pythondate(self.year, self.month, self.day) + timedelta(nbr_days)
            return BankDate(result)

    def find_next_banking_day(self, nextday=1, holidaylist=()):
        
        if nextday not in (-1, 1):
            raise BankDateError(
            'The nextday must be  in (-1, 1), not %s of type %s'
            % (nextday, type(nextday)))
        lst = [BankDate(d).__str__() for d in holidaylist]
        date = self
        for i in range(30):
            if date.isoweekday() < 6 and str(date) not in lst:
                break
            date = date.add_days(nextday)
        return date

    def adjust_to_bankingday(self, daterolling='Actual', holidaylist=()):
        

        def actual_daterolling(holidaylist):
            '''Implement date rolling method Actual, ie no change
            '''
            return self

        def following_daterolling(holidaylist):
            '''Implement date rolling method Following
            '''
            return self.find_next_banking_day(1, holidaylist)

        def previous_daterolling(holidaylist):
            '''Implement date rolling method Previous
            '''
            return self.find_next_banking_day(-1, holidaylist)

        def modified_following_daterolling(holidaylist):
            '''Implement date rolling method Modified Following
            '''
            next_bd = self.find_next_banking_day(1, holidaylist)
            if self.month == next_bd.month:
                return next_bd
            else:
                return self.find_next_banking_day(-1, holidaylist)

        def modified_previous_daterolling(holidaylist):
            '''Implement date rolling method Modified Previous
            '''
            next_bd = self.find_next_banking_day(-1, holidaylist)
            if self.month == next_bd.month:
                return next_bd
            else:
                return self.find_next_banking_day(1, holidaylist)

        daterolling_dict = {
            'Actual':             actual_daterolling,
            'Following':          following_daterolling,
            'Previous':           previous_daterolling,
            'ModifiedFollowing':  modified_following_daterolling,
            'ModifiedPrevious':   modified_previous_daterolling,
            }
        if daterolling in daterolling_dict.keys():
            return daterolling_dict[daterolling](holidaylist)
        else:
            raise BankDateError(
            'The daterolling must be one of %s, not %s of type %s' \
            % (daterolling_dict.keys(), daterolling, type(daterolling)))

    def weekday(self, as_string=False):
        '''
        :param as_string: Return weekday as a number or a string
        :type as_string: Boolean
        :Return: day as a string or a day number of week, 0 = Monday etc
        '''
        if as_string:
            return self.strftime('%a')
        else:
            return self.weekday()

    def first_day_in_month(self):
        ''':Return: first day in month for this BankDate as BankDate
        '''
        day = self.day
        return self + '%sd' % (1 - day)

    def next_imm_date(self, future=True):
        '''An IMM date is the 3. wednesday in the months march, june,
        september and december

        reference: http://en.wikipedia.org/wiki/IMM_dates

        :Return: Next IMM date for BankDate as BankDate
        '''
        month = self.month
        if future:
            add_month = 3 - (month % 3)
        else:
            add_month = - ((month % 3) or 3)
        # First day in imm month
        out_date = self.first_day_in_month() + '%sm' % add_month
        add_day = 13 + (9 - out_date.weekday()) % 6
        out_date += '%sd' % add_day
        return out_date

    def nbr_of_months(self, date):
        '''
        :param date: date
        :type date: BankDate
        :return: The number of months between this bankingday and a date
        '''
        date = BankDate(date)
        if self.__str__() < date.__str__():
            date_min, date_max = self, date
            sign = +1
        else:
            date_min, date_max = date, self
            sign = -1
        nbr_month = (date_max.year - date_min.year) * 12 \
                    + date_max.month - date_min.month
        if date_max.day >= date_min.day:
            return sign * nbr_month
        else:
            return sign * (nbr_month - 1)

    def nbr_of_years(self, date):
        '''
        :param date: date
        :type date: BankDate
        :return: The number of years between this bankingday and a date
        '''
        nom = self.nbr_of_months(date)
        if nom > 0:
            return int(nom / 12)
        else:
            return - int(-nom / 12)

    def nbr_of_days(self, value):
        '''
        :param date: date
        :type date: BankDate
        :return: The number of days between this bankingday and a date
        '''
        bankdate = BankDate(value)
        if bankdate:
            # Subtraction is defined for _pythondate
            return -super(BankDate, self).__sub__(bankdate).days


def daterange_iter(enddate_or_integer,start_date=BankDate(),step='1y',
    keep_start_date=True,daterolling='Actual',holidaylist=()):
    
    s_date = BankDate(start_date)
    step = TimePeriod(step)
    if isinstance(enddate_or_integer,  int):
        e_date = s_date + enddate_or_integer * step
    else:
        e_date = BankDate(enddate_or_integer)
    if e_date < s_date:
        s_date, e_date = e_date, s_date
    step.count = -abs(step.count)
    nbr_periods = 0
    tmp_date = e_date
    while tmp_date > s_date:
        yield tmp_date.adjust_to_bankingday(daterolling, holidaylist)
        nbr_periods += 1
        tmp_date = e_date + nbr_periods * step
    if keep_start_date:
        yield s_date.adjust_to_bankingday(daterolling, holidaylist)


def daterange(enddate_or_integer,start_date=BankDate(),step='1y',
    keep_start_date=True,daterolling='Actual',holidaylist=()):
    
    return sorted(daterange_iter(enddate_or_integer, start_date, step,keep_start_date, daterolling, holidaylist))


def period_count(end_date, start_date=BankDate(), period='1y'):

    return len(list(daterange_iter(end_date,  start_date, period,  False)))

if __name__ == '__main__':
    import doctest
    doctest.testmod()


def strips_data_generation():
    """Retrieves STRIPS data from US Treasuries or UK Gilts.
    Returns a clean DataFrame of the yields across all available maturity dates.

    Given access to more frequent data then prior trading day end,
    will update to use interday updated strips data.

    This should be a much quicker process since the get from a dedicated 
    data source will be faster than an pulling down and regex parsing the 
    raw html data.

    A proper HF data source will likely return XML or JSON formatted 
    responses which can be unpacked via several different python libraries
    and remove the need for the regex below.

    The process would ideally be run outside the critical path and the 
    resulting data referenced from within the function itself.
    """

    bond_portfolio_currency = input('What currency is the bond portfolio in? USD or GBP? ').upper()
    if bond_portfolio_currency == 'GBP':
        page = requests.get('http://www.dmo.gov.uk/xmlData.aspx?rptCode=D3B.2&page=Gilts/Daily_Prices')
        if page.status_code==200:
            base_data_location_string = ('/Users/baronabramowitz/Desktop/todays_strips_data_raw' 
                                        + str(datetime.now()))
            raw_xml = open(base_data_location_string,'w')
            #raw_xml = open('/Users/baronabramowitz/Desktop/todays_strips_data_raw','w')
            raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)
            raw_xml.close()
        else:
            print("link invalid")

        pattern = re.compile("INSTRUMENT_NAME=\"Treasury Coupon Strip \d{2}[a-zA-Z]{3}2\d{3}\" REDEMPTION_DATE=\"(2\d{3}[-][0-1][0-9][-][0-3][0-9])T.{157}YIELD=\"(\d{1,2}\.\d{12})\"")
        pattern_g1_matches = []
        pattern_g2_matches = []
        match_list = []
        for i, line in enumerate(open(base_data_location_string, 'r')): 
            for match in re.finditer(pattern, line):
                match_list.append(match)
                pattern_g1_matches.append(match.group(1))
                pattern_g2_matches.append(match.group(2))
        pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
        pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
        strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df,left_index=True,right_index = True)
        strips_output.columns = ['Date','Yield']
        strips_output['Date'] = pd.to_datetime(strips_output['Date'])
        strips_output = strips_output.sort_values('Date')
        strips_output.index = range(0,len(strips_output))
        return strips_output

    elif bond_portfolio_currency == 'USD':
        page = requests.get('http://online.barrons.com/mdc/public/page/9_3020-tstrips.html?mod=bol_topnav_9_3000')
        if page.status_code==200:
            base_data_location_string = '/Users/baronabramowitz/Desktop/todays_us_strips_data_raw' + str(datetime.now())
            raw_xml = open(base_data_location_string,'w')
            raw_xml.write('Download Timestamp: ' + str(datetime.now()) + page.text)         
            raw_xml.close()
        else:
            print("link invalid")

        pattern_date = re.compile(r"<td class=\"text\">(2[0-9]{3} [a-zA-z]{3} [0-3][0-9])</td>")
        pattern_yield = re.compile(r"<td style=\"border-right:0px\" class=\"num\">([0-9]{1,2}\.[0-9]{2})</td>")
        pattern_g1_matches = []
        pattern_g2_matches = []
        match_list = []
        for i, line in enumerate(open(base_data_location_string, 'r')): 
            if i > 2480:
                for match in re.finditer(pattern_date, line):
                    match_list.append(match)
                    pattern_g1_matches.append(match.group(1))
            else:
                pass

        for i, line in enumerate(open(base_data_location_string, 'r')):
            if i > 2480:
                for match in re.finditer(pattern_yield, line):
                    match_list.append(match)
                    pattern_g2_matches.append(match.group(1))
            else:
                pass
        print (match_list)
        print (pattern_g1_matches)
        print (pattern_g2_matches)
        pattern_g1_matches_df = pd.DataFrame(pattern_g1_matches)
        pattern_g2_matches_df = pd.DataFrame(pattern_g2_matches)
        strips_output = pd.merge(pattern_g1_matches_df,pattern_g2_matches_df, left_index=True, right_index = True)
        strips_output.columns = ['Date','Yield']
        strips_output['Date'] = pd.to_datetime(strips_output['Date'])
        strips_output = strips_output.sort_values('Date')
        strips_output.index = range(0,len(strips_output))
        return strips_output


#todays_strips_data = strips_data_generation()


def nearest_date(entered_date):
    """Return nearest date from list of STRIPS maturity dates."""
    # This function works but is certainly very hacky and unelegant. 
    # There must be a better way to perfrom this task than using this dictionary lookup
    
    dates = todays_strips_data['Date'].tolist() #  Input for dates, returned from strips parsing functions
    day_diffs = {}
    for i, date in enumerate(dates):
        day_diffs.update({i:abs(BankDate(date).nbr_of_days(entered_date))})
    return dates[int(min(day_diffs, key=day_diffs.get)) - 1]


def payment_dates(dateval, step):
    '''Generates the dates on which payments (coupon & principal) occur given maturity date

    Steps in number of months e.g. '6m', '3m', '24m'
    Default is semi-annual compounding
    '''

    new_dates = []
    for date in daterange(dateval, step ='6m'):
        if datetime.weekday(date) == 6:
            date = date + '1d'
            new_dates.append(date)
        elif datetime.weekday(date) == 5:
            date = date + '2d'
            new_dates.append(date)
        else:
            new_dates.append(date)
    del new_dates[0]
    return(new_dates)


def yields_for_payment_dates(new_dates):
    """Generates list of discount rates for coupon payment dates

    **Requires the output of strips_data_generation assigned to todays_strips_data 
    to be in memory before this process will function properly**
    """

    payment_date_approximate_yields = []
    for date in new_dates:
        payment_date_approximate_yields.append(float((todays_strips_data.loc[
            todays_strips_data['Date'] == nearest_date(date)]).iloc[0]['Yield']))
    return payment_date_approximate_yields


def days_to_payment(mat_date, pay_step):
    '''Returns a list of days until coupon dates

    Takes the payment dates outputted from payment_dates 
    and converts them into a day count from the current day (or next business day when appropriate)
    to the date of the respective payment
    '''

    step = pay_step
    dateval = mat_date
    new_dates = payment_dates(dateval, step)
    days_to_payment = []
    for date in new_dates:
        days = BankDate().nbr_of_days(date)
        days_to_payment.append(days)
    return days_to_payment    


def value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type):
    """Values bond given current inputs."""

    pv_fcf = []
    payment_step = str(payments_per_year/12) + 'm'
    discount_rates = yields_for_payment_dates(payment_dates(maturity_date, payment_step))
    days_to_payments = days_to_payment(maturity_date,payment_step)

    # Currently bond premiums are hard coded but a more scalable version
    # would include these premiums being stored elsewhere and referenced 
    # within the function; this would allow for distributing the bond valuations
    # across multiple processors when valuign a portfolio.
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

    bond_maturity_remaining = (BankDate().nbr_of_days(maturity_date))/365

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


def value_bond_var(face_value,maturity_date,coupon_rate,payments_per_year,discount_rate):
    """Values bond for value at risk function"""

    pv_fcf = []
    bond_maturity_remaining = (BankDate().nbr_of_days(maturity_date))/365
    payment_step = str(payments_per_year/12) + 'm'
    if payments_per_year == 0:
        coupon_payment = 0
    else:
        coupon_payment = ((coupon_rate/100)*face_value)/payments_per_year
    days_to_payments = days_to_payment(maturity_date,payment_step)

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


def value_portfolio(csv_location):
    """Calculates the value of a portfolio of bonds (as a CSV)"""

    bond_val_portfolio = []
    bond_maturity_set = []
    portfolio = generate_portfolio(csv_location)

    for bond in zip(portfolio['face_value'],portfolio['maturity_date'],portfolio['coupon_rate'],
                   portfolio['payments_per_year'],portfolio['bond_rating'],portfolio['bond_type']
                ):
        bond_maturity_set.append(value_bond(*bond)[3])
        bond_val_portfolio.append(value_bond(*bond)[0])

    portfolio_val = sum(bond_val_portfolio)
    return {'Portfolio Value':portfolio_val, 'Set of Bond Values' : bond_val_portfolio, 'Set of Bond Maturities' : bond_maturity_set}


def duration_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type):
    """Calculates the duration and Macaulay/Modified duration"""

    value_bond_output_db = value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type)
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
    portfolio = generate_portfolio(csv_location)
    val_portfolio_output = value_portfolio(csv_location)

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


def convexity_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type):
    """Calculates the convexity of an indivudal bond"""

    value_bond_output_cb = value_bond(face_value,maturity_date,coupon_rate,payments_per_year,bond_rating,bond_type)
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
    portfolio = generate_portfolio(csv_location)
    val_portfolio_output = value_portfolio(csv_location)

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


class TestSuite(unittest.TestCase):
     """Large Selection of Tests for the above code"""
     def test_portfolio_VaR(self):
        self.assertEqual({'Portfolio VaR Percent': 6.5004978313881256, 'Portfolio VaR': 417084.6525381055},
            value_at_risk_portfolio_set('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv', 95))
     def test_bond_convexity(self):
         self.assertEqual({'Bond Convexity': 36.36653523348562},
                convexity_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
     def test_portfoio_convexity(self):
         self.assertEqual({'Portfolio Convexity': 143.72975134873602},
            convexity_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
     def test_duration_portfolio(self):
         self.assertEqual({'Portfolio Duration': 11.093967137303755, 'Modified Portfolio Duration': 11.048514534591584}
            ,duration_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
     def test_value_portfolio(self):
         self.assertEqual({'Set of Bond Values': [11320.188859642592, 42745.647831637427, 3902833.9817734361, 
            275809.67525298434, 831588.72828977392, 403632.83643454808, 554517.6557094187, 393746.83512144675], 
            'Set of Bond Maturities': [5.8191780821917805, 8.923287671232877, 12.378082191780821, 1.5753424657534247, 
            7.96986301369863, 17.232876712328768, 11.487671232876712, 10.2], 
            'Portfolio Value': 6416195.5492728874},
            value_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
     def test_bond_dur(self):
        #Checks if bond duration properly calculates
        self.assertEqual({'Modified Duration': 5.447036192738801, 'Bond Duration': 5.455872780654858},
            duration_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA','Corporate'))
     def test_bond_val(self):
        #Checks if bond value properly calculates
        self.assertEqual((11321.928444124125, [124.92962437224833, 124.8759248234797, 124.82520284124303, 
            124.76929655187979, 124.69524141994178, 124.59769289760095, 124.46073934338344, 124.27685339815154, 
            124.03101248430148, 123.72361917185522, 123.33685616967725, 9953.406380650362], [116, 298, 481, 663, 
            848, 1030, 1212, 1394, 1577, 1759, 1942, 2124], 5.8191780821917805, [0.17720275999999996, 
            0.12163759999999998, 0.106188285, 0.10170096999999999, 0.10506873999999998, 0.11423621999999999, 
            0.13020216999999998, 0.15191707999999998, 0.180118855, 0.21297338999999998, 0.25175044999999996, 0.29373288]),
        value_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))


if __name__ == "__main__":
    todays_strips_data = strips_data_generation()
    #nearest_date('2022-06-18')
    #print(todays_strips_data)
    #yields_for_payment_dates(payment_dates('2022-06-18','6m'))
    #print(yields_for_payment_dates(payment_dates('2022-06-18','6m')))
    """
    print(value_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
    print(generate_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
    print(value_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
    print(duration_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
    print(duration_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
    print(convexity_bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate'))
    print(convexity_portfolio('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv'))
    print(value_at_risk_portfolio_set('/Users/baronabramowitz/Desktop/bond_portfolio_data.csv',95))
    """
    unittest.main()
        


 











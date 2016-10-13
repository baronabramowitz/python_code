__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '22/08/2016'

import re
from datetime import date as _pythondate
from datetime import timedelta, datetime
from abc import ABCMeta, abstractmethod


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
    return len(list(daterange_iter(end_date, start_date, period, False)))
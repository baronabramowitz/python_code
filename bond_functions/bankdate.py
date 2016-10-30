__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '15/10/2016'

from datetime import date as _pythondate
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TimePeriod(object):
    # Likely would be improved as a named tupel

    def __init__(self, period):
        self.period = period
        self.count = float(period[:-1])
        self.unit = period[-1:]


class BankDate(object):

    def __init__(self, bank_date=_pythondate.today()):
        try:
            self.bank_date = datetime.strptime(bank_date, '%Y-%m-%d').date()
        except TypeError:
            self.bank_date = bank_date
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        # Ensure not weekend
        if datetime.weekday(self.bank_date) == 6:
            self.bank_date = self.bank_date + relativedelta(days=1)
        elif datetime.weekday(self.bank_date) == 5:
            self.bank_date = self.bank_date + relativedelta(days=2)
        else:
            pass
            # self.bank_date = bank_date **FIXED**
            # Above code caused bank_date to be a string

    def _add(self, period):
        """A TimePeriod can be added to a BankDate"""

        period_count = int(float(period[:-1]))
        period_unit = period[-1:]
        # rd_input = {'y' : 'years','m' : 'months','w' : 'weeks','d' : 'days'}[period[-1:]]
        # return self.bank_date + relativedelta(**{rd_input : period_count})
        # Below code is more efficient than above dict method
        if period_unit == 'y':
            return self.bank_date + relativedelta(years=period_count)
        elif period_unit == 'm':
            return self.bank_date + relativedelta(months=period_count)
        elif period_unit == 'w':
            return self.bank_date + relativedelta(weeks=period_count)
        elif period_unit == 'd':
            return self.bank_date + relativedelta(days=period_count)

    def __str__(self):
        return str(self.bank_date)

    def __repr__(self):
        return str(self.bank_date)

    def _sub(self, period):
        """A TimePeriod can be subtracted from a BankDate"""

        period_count = int(float(period[:-1]))
        period_unit = period[-1:]
        # rd_input = {'y' : 'years','m' : 'months','w' : 'weeks','d' : 'days'}[period[-1:]]
        # return self.bank_date - relativedelta(**{rd_input : period_count})
        # Below code is more efficient than above dict method
        if period_unit == 'y':
            return self.bank_date - relativedelta(years=period_count)
        elif period_unit == 'm':
            return self.bank_date - relativedelta(months=period_count)
        elif period_unit == 'w':
            return self.bank_date - relativedelta(weeks=period_count)
        elif period_unit == 'd':
            return self.bank_date - relativedelta(days=period_count)

    def num_of_days(self, fut_date):
        """Return the number of days between a future date and today(or the next BankDate)"""
        try:
            return (fut_date - self.bank_date).days
        except TypeError:
            return (fut_date.bank_date - self.bank_date).days

class DateSub(object):
    """Class used just for subtracting relativedeltas from datetime objects
    
    Created in order to solve issue with date_range where use of BankDate
    class to iterate backwards caused issues with payment dates being 
    iterated backwards including movements to weekdays, needed to apply weekend
    validation only after the initial dates had been created
    """
    def __init__(self, sub_date):
        try:
            self.sub_date = datetime.strptime(sub_date, '%Y-%m-%d').date()
        except TypeError:
            self.sub_date = sub_date
            # self.bank_date = bank_date **FIXED**
            # Above code caused bank_date to be a string
    def _sub(self, period):
        """A TimePeriod can be subtracted from a SubDate"""

        period_count = int(float(period[:-1]))
        period_unit = period[-1:]
        if period_unit == 'y':
            return self.sub_date - relativedelta(years=period_count)
        elif period_unit == 'm':
            return self.sub_date - relativedelta(months=period_count)
        elif period_unit == 'w':
            return self.sub_date - relativedelta(weeks=period_count)
        elif period_unit == 'd':
            return self.sub_date - relativedelta(days=period_count)


def date_range(enddate, step, startdate=_pythondate.today()):
    """Return a set of dates iterating back from enddate by step
    
    This is very, very hacky. It really shouldn't switch between classes.
    However, it works and is only run once per bond upon the class init.
    Could really use a second set of eyes.
    """

    _date = DateSub(enddate.bank_date)
    date_list = [enddate]
    while _date.sub_date > startdate:
        _date = _date._sub(step)
        date_list.append(BankDate(_date))
        _date = DateSub(_date)
    del date_list[-1]
    return date_list


if __name__ == "__main__":
    # print(_pythondate.today())
    #three_yearsf = BankDate()._add('3y')
    #three_yearsb = BankDate()._sub('3y')

    # print(three_yearsb)
    print(BankDate().num_of_days(BankDate('2022-06-15')))
    # for i in date_range('2022-06-15', '6m'):
    #    print(str(i), type(i))

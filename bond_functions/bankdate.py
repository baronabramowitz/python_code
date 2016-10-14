__author__ = 'Baron Abramowitz'
__version__ = '0.1.0'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '22/08/2016'

from datetime import date as _pythondate
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

class TimePeriod(object):
    def __init__(self, period):
        self.period = period
        self.count = int(period[:-1])
        self.unit = period [-1:]

class BankDate(object):
    def __init__(self, bank_date = _pythondate.today()):
        if isinstance(bank_date, str):
            self.bank_date = datetime.strptime(bank_date, '%Y-%m-%d').date()
            print(type(self.bank_date))
        else:    
            self.bank_date = bank_date
        # Ensure not weekend 
        if datetime.weekday(self.bank_date) == 6:
            self.bank_date = bank_date + relativedelta(days = 1)
        elif datetime.weekday(self.bank_date) == 5:
            self.bank_date = bank_date + relativedelta(days = 2) 
        else:
            self.bank_date = bank_date
    
    def _add(self, period):
        """A TimePeriod can be added to a BankDate"""
        period = TimePeriod(period)
        if period.unit == 'y':
            return self.bank_date + relativedelta(years = period.count)
        elif period.unit == 'm':
            return self.bank_date + relativedelta(months = period.count)
        elif period.unit == 'w':
            return self.bank_date + relativedelta(weeks = period.count)
        elif period.unit == 'd':
            return self.bank_date + relativedelta(days = period.count)
    def __str__ (self):
        return str(self.bank_date)
    
    def _sub(self, period):
        """A TimePeriod can be added to a BankDate"""
        period = TimePeriod(period)
        if period.unit == 'y':
            return self.bank_date - relativedelta(years = period.count)
        elif period.unit == 'm':
            return self.bank_date - relativedelta(months = period.count)
        elif period.unit == 'w':
            return self.bank_date - relativedelta(weeks = period.count)
        elif period.unit == 'd':
            return self.bank_date - relativedelta(days = period.count)

    def num_of_days(self, fut_date):
        """Return the number of days between a future date and today(or the next BankDate)"""
        return (fut_date.bank_date - self.bank_date).days

def date_range(enddate, step,  startdate = BankDate()):
    #step = TimePeriod(step)
    enddate = datetime.strptime(enddate, '%Y-%m-%d').date()
    _date = BankDate(enddate)
    date_list = [BankDate(enddate)]
    while _date.bank_date > startdate.bank_date:
        _date = BankDate(_date._sub(step))
        date_list.append(_date)
    return date_list

 
if __name__ == "__main__":
    #print(_pythondate.today())
    #three_years = BankDate()._add('3y')
    #print(three_years)
    for i in date_range('2022-06-15', '6m'):
        print(str(i), type(i))
__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '15/10/2016'

import date_functions as df
import bankdate as BD
from math import exp


class Bond(object):
    """Class to build a bond out of attributes

    Attributes include:
    Face Value,
    Maturity Date,
    Coupon Rate,
    Payment/coupon Frequency (Expressed as payments per year),
    Bond Rating (AAA to A currently, will add more),
    Bond Type (Government or Corporate)

    Will also add currency attributes
    Trailing _c is for continuous compounding
    """

    # pylint: disable=R0904
    def __init__(self, face_value, maturity_date, coupon_rate, payments_per_year, rating, btype):
        self.face_value = float(face_value)
        self.maturity_date = BD.BankDate(maturity_date)
        self.coupon_rate = float(coupon_rate)
        self.payments_per_year = int(payments_per_year)
        self.rating = rating
        self.btype = btype
        try:
            self.payment_dates = BD.date_range(
                self.maturity_date, (str(12 / self.payments_per_year) + 'm'))
        except ZeroDivisionError:
            self.payment_dates = self.maturity_date

    def __repr__(self):
        if self.payments_per_year == 1:
            pay_freq = 'Annual'
        if self.payments_per_year == 2:
            pay_freq = 'Semi annual'
        if self.payments_per_year == 4:
            pay_freq = 'Quarterly'
        if self.payments_per_year == 12:
            pay_freq = 'Monthly'
        if self.payments_per_year == 52:
            pay_freq = 'Weekly'
        if self.payments_per_year == 365:
            pay_freq = 'Daily'
        return "%s %s%s %s %s" % (
            self.btype, str(self.coupon_rate), '%', self.maturity_date, pay_freq)

    def days_to_payments(self):
        """Generate the set of days to each payment"""
        return df.days_to_payment(self.payment_dates)

    def update_rating(self, new_rating):
        """Update the rating for a specific bond"""
        self.rating = new_rating

    def rating_premium(self):
        """Set the rating premium above the discount rates for different bond ratings/types"""
        rating_dict = {'Corporate': {'AAA': .015, 'AA': .025, 'A': .035},
                       'Government': {'AAA': 0, 'AA': .015, 'A': .025}}
        return rating_dict[self.btype][self.rating]

    def discount_rates(self):
        """Generate a set of discount rates for each of the payment dates"""
        return df.yields_for_payment_dates(self.payment_dates)

    def discount_rates_var(self, scenario_spl):
        """Generate a set of discount rates for each of the payment dates"""
        return df.yields_for_payment_dates_var(self.payment_dates, scenario_spl)

    def maturity_remaining(self):
        """Generate the maturity remaining in years for a single bond"""
        return ((BD.BankDate().num_of_days(self.maturity_date)) / 365)

    def coupon_payment(self):
        """Calculate the coupon payment for each payment date for the bond"""
        try:
            return ((self.coupon_rate / 100) *
                    self.face_value) / self.payments_per_year
        except ZeroDivisionError:
            return 0

    def present_value_fcf(self):
        """Calculate the present value of each cash flow for a bond using daily compounding"""

        # Currently hard coded for Actual/365 day count but can be updated to
        # reflect other conventions.
        pv_fcf = []
        # Could have made this a list comprehansion but it would be much less
        # clear

        discount_rates = [x * (1 + self.rating_premium())
                          for x in self.discount_rates()]
        try:
            dtp = self.days_to_payments()
            for i, day_count in enumerate(dtp):
                if day_count == max(dtp):
                    pv_cf = (self.coupon_payment() + self.face_value) / \
                        ((1 + (discount_rates[i] / 100 / 365))**day_count)
                    pv_fcf.append(pv_cf)
                elif day_count != 0 and day_count != max(dtp):
                    pv_cf = self.coupon_payment() / \
                        ((1 + (discount_rates[i] / 100 / 365))**day_count)
                    pv_fcf.append(pv_cf)
                else:
                    pass
        except TypeError:
            pv_fcf.append(self.face_value /
                          ((1 + (discount_rates[0] / 100 / 365))**BD.BankDate().num_of_days(self.maturity_date)))
        return pv_fcf

    def present_value_fcf_c(self):
        """Calculate the present value of each cash flow for a bond using continuous compounding"""

        # Currently hard coded for Actual/365 day count but can be updated to
        # reflect other conventions.
        pv_fcf = []
        # Could have made this a list comprehansion but it would be much less
        # clear
        discount_rates = [x * (1 + self.rating_premium())
                          for x in self.discount_rates()]
        try:
            dtp = self.days_to_payments()
            for i, day_count in enumerate(dtp):
                if day_count == max(dtp):
                    pv_cf = (self.coupon_payment() + self.face_value) * \
                        exp(-(discount_rates[i] / 100)
                            * (day_count / 365))
                    pv_fcf.append(pv_cf)
                elif day_count != 0 and day_count != max(dtp):
                    pv_cf = self.coupon_payment() * \
                        exp(-(discount_rates[i] / 100) * (day_count / 365))
                    pv_fcf.append(pv_cf)
                else:
                    pass
        except TypeError:
            pv_fcf.append(self.face_value * exp(-(discount_rates[0] / 100)
                                                * (self.maturity_remaining())))
        return pv_fcf

    def present_value_fcf_var(self, scenario_spl):
        """Calculate the present value of each cash flow for a bond using daily compounding"""

        # Currently hard coded for Actual/365 day count but can be updated to
        # reflect other conventions.
        pv_fcf = []
        # Could have made this a list comprehansion but it would be much less
        # clear
        discount_rates = [x * (1 + self.rating_premium())
                          for x in self.discount_rates_var(scenario_spl)]
        try:
            dtp = self.days_to_payments()
            for i, day_count in enumerate(dtp):
                if day_count == max(dtp):
                    pv_cf = (self.coupon_payment() + self.face_value) / \
                        ((
                            1 + (discount_rates[i] / 100 / 365))**day_count)
                    pv_fcf.append(pv_cf)
                elif day_count != 0 and day_count != max(dtp):
                    pv_cf = self.coupon_payment() / \
                        ((
                            1 + (discount_rates[i] / 100 / 365))**day_count)
                    pv_fcf.append(pv_cf)
                else:
                    pass
        except TypeError:
            pv_fcf.append(self.face_value /
                          ((1 + (discount_rates[0] / 100 / 365))**BD.BankDate().num_of_days(self.maturity_date)))
        return pv_fcf

    def present_value_fcf_c_var(self, scenario_spl):
        """Calculate the present value of each cash flow for a bond using continuous compounding"""

        # Currently hard coded for Actual/365 day count but can be updated to
        # reflect other conventions.
        pv_fcf = []
        # Could have made this a list comprehansion but it would be much less
        # clear
        discount_rates = [x * (1 + self.rating_premium())
                          for x in self.discount_rates_var(scenario_spl)]
        try:
            dtp = self.days_to_payments()
            for i, day_count in enumerate(dtp):
                if day_count == max(dtp):
                    pv_cf = (self.coupon_payment() + self.face_value) * \
                        exp(-(discount_rates[i] / 100)
                            * (day_count / 365))
                    pv_fcf.append(pv_cf)
                elif day_count != 0 and day_count != max(dtp):
                    pv_cf = self.coupon_payment() * \
                        exp(-(discount_rates[i] / 100)
                            * (day_count / 365))
                    pv_fcf.append(pv_cf)
                else:
                    pass
        except TypeError:
            pv_fcf.append(self.face_value * exp(-(discount_rates[0] / 100)
                                                * (self.maturity_remaining())))
        return pv_fcf

    def value(self):
        """Calculate the value of a Bond object using daily compounding"""
        return sum(self.present_value_fcf())

    def value_c(self):
        """Calculate the value of a Bond object using continuous compounding"""
        return sum(self.present_value_fcf_c())

    def value_var(self, scenario_spl):
        """Calculate the value of a Bond object using daily compounding"""
        return sum(self.present_value_fcf_var(scenario_spl))

    def value_c_var(self, scenario_spl):
        """Calculate the value of a Bond ob_ject using continuous compounding"""
        return sum(self.present_value_fcf_c_var(scenario_spl))

    def duration(self):
        """Calculate the duration of a Bond object using daily compounding"""
        try:
            years_to_payments = [
                days / 365 for days in self.days_to_payments()]
            intermediate_dur_calcs = [
                (cf[0] * cf[1]) for cf in zip(self.present_value_fcf(), years_to_payments)]
            return sum(intermediate_dur_calcs) / self.value()
        except TypeError:
            return self.maturity_remaining()

    def duration_c(self):
        """Calculate the duration of a Bond object using continuous compounding"""
        try:
            years_to_payments = [
                days / 365 for days in self.days_to_payments()]
            intermediate_dur_calcs = [
                (cf[0] * cf[1]) for cf in zip(self.present_value_fcf_c(), years_to_payments)]
            return sum(intermediate_dur_calcs) / self.value_c()
        except TypeError:
            return self.maturity_remaining()

    def modified_duration(self):
        """Calculate the modified duration of a Bond object using daily compounding"""
        return self.duration() / (1 + sum(self.discount_rates()) / len(self.discount_rates()) / 100)

    def modified_duration_c(self):
        """Calculate the modified duration of a Bond object using continuous compounding"""
        return (self.duration_c() / (1 + sum(self.discount_rates())
                                     / len(self.discount_rates()) / 100))

    def convexity(self):
        """Calculate the convexity of an indivudal bond using daily compounding"""
        try:
            years_to_payments = [
                days / 365 for days in self.days_to_payments()]
            intermediate_conv_calcs = [((pv_cf[0]) * (pv_cf[1]**2 + pv_cf[1]))
                                       for pv_cf in zip(self.present_value_fcf(), years_to_payments)]
            return (sum(intermediate_conv_calcs) /
                    (self.value() * (1 + sum(self.discount_rates())
                                     / len(self.discount_rates()) / 100)**2))
        except TypeError:
            t = self.maturity_remaining()
            return ((self.face_value * (t**2 + t) / (1 + self.discount_rates()[0] / 100)**t)
                    / (self.value() * (1 + self.discount_rates()[0] / 100)**2))

    def convexity_c(self):
        """Calculate the convexity of an indivudal bond using continuous compounding"""
        try:
            years_to_payments = [
                days / 365 for days in self.days_to_payments()]
            intermediate_conv_calcs = [((pv_cf[0]) * (pv_cf[1]**2 + pv_cf[1]))
                                       for pv_cf in zip(self.present_value_fcf_c(), years_to_payments)]
            return (sum(intermediate_conv_calcs) /
                    (self.value_c() * (1 + sum(self.discount_rates())
                                       / len(self.discount_rates()) / 100)**2))
        except TypeError:
            t = self.maturity_remaining()
            return (self.face_value * (t**2 + t) * exp(-(self.discount_rates()[0] / 100) * t)
                    / (self.value() * (1 + self.discount_rates()[0] / 100)**2))


if __name__ == "__main__":
    bond1 = Bond(10000.0, '2022-06-15', 2.5, 2, 'AAA', 'Corporate')
    print(bond1)

    print(bond1.value())
    print(bond1.value_c())
    print((bond1.value_c() / bond1.value()) * 100)

    print(bond1.duration())
    print(bond1.duration_c())
    print((bond1.duration_c() / bond1.duration()) * 100)

    print(bond1.convexity())
    print(bond1.convexity_c())
    print((bond1.convexity_c() / bond1.convexity()) * 100)

    print(bond1.face_value)
    print(bond1.maturity_date)
    print(bond1.coupon_rate)
    print(bond1.payments_per_year)
    print(bond1.rating)
    print(bond1.btype)

__author__ = 'Baron Abramowitz'
__maintainer__ = 'Baron Abramowitz'
__email__ = 'baron.abramowitz@yahoo.com'
__date__ = '03/10/2016'

import date_functions as df
import BankDate_ as BD
from math import exp

class Bond(object):
	"""Trailing _c is for continuous compounding"""
	def __init__(self, face_value,maturity_date,coupon_rate,payments_per_year,rating,btype):
		self.face_value = face_value
		self.maturity_date = maturity_date
		self.coupon_rate = coupon_rate
		self.payments_per_year = payments_per_year
		self.rating = rating
		self.btype = btype

	def days_to_payments(self):
		"""Generates the set of days to each payment"""
		payment_step = str(self.payments_per_year/12) + 'm'
		days_to_payments = df.days_to_payment(self.maturity_date,payment_step)
		return	days_to_payments

	def update_rating(self, new_rating):
		"""Update the rating for a specific bond"""
		self.rating = new_rating

	def rating_premium(self):
		"""Sets the rating premium above the discount rates for different bond ratings/types"""
		if self.btype == 'Corporate':
		    if self.rating == 'AAA':
		        rating_premium = .015
		    elif self.rating == 'AA':
		        rating_premium = .025
		    elif self.rating == 'A':
		        rating_premium = .035
		    else:
		        pass
		elif self.btype == 'Government':
		    if self.rating == 'AAA':
		        rating_premium = 0
		    elif self.rating == 'AA':
		        rating_premium = .015
		    elif self.rating == 'A':
		        rating_premium = .025
		    else:
		        pass
		else:
		    pass
		return rating_premium



	def discount_rates(self):
		"""Generates a set of discount rates for each of the payment dates"""
		payment_step = str(self.payments_per_year/12) + 'm'
		#discount_rates = df.yields_for_payment_dates(df.payment_dates(self.maturity_date, payment_step))
		discount_rates = df.yields_for_payment_dates_(self.maturity_date, payment_step)
		return discount_rates

	def maturity_remaining(self):
		"""Generates the maturity remaining in years for a single bond"""
		return (BD.BankDate().nbr_of_days(self.maturity_date))/365

	def coupon_payment(self):
		"""Claculates the coupon payment for each payment date for the bond"""
		if self.payments_per_year == 0:
			coupon_payment = 0
		else:
			coupon_payment = ((self.coupon_rate/100)*self.face_value)/self.payments_per_year
		return coupon_payment

	def present_value_fcf(self):
		"""Currently hard coded for Actual/365 day count but can be updated to reflect other conventions.
		Using daily compounding.
		"""
		pv_fcf = []
		discount_rates = [x * (1 + self.rating_premium()) for x in self.discount_rates()]
		for i, day_count in enumerate(self.days_to_payments()):
			if day_count == max(self.days_to_payments()):
				pv_cf = (self.coupon_payment() + self.face_value)/((1+(discount_rates[i]/100/365))**day_count)
				pv_fcf.append(pv_cf)
			elif day_count != 0 and day_count != max(self.days_to_payments()):
				pv_cf = self.coupon_payment()/((1+(discount_rates[i]/100/365))**day_count)
				pv_fcf.append(pv_cf)
			else:
				pass
		return pv_fcf

	def present_value_fcf_c(self):
		"""Currently hard coded for Actual/365 day count but can be updated to reflect other conventions.
		Using continuous compounding.
		"""
		pv_fcf = []
		discount_rates = [x * (1 + self.rating_premium()) for x in self.discount_rates()]
		for i, day_count in enumerate(self.days_to_payments()):
			if day_count == max(self.days_to_payments()):
				pv_cf = (self.coupon_payment() + self.face_value) * exp(-(discount_rates[i]/100) * (day_count/365))
				pv_fcf.append(pv_cf)
			elif day_count != 0 and day_count != max(self.days_to_payments()):
				pv_cf = self.coupon_payment() * exp(-(discount_rates[i]/100) * (day_count/365))
				pv_fcf.append(pv_cf)
			else:
				pass
		return pv_fcf
	        
	   
	def value(self):
		"""Calculates the value of a Bond object using daily compounding"""
		return sum(self.present_value_fcf())

	def value_c(self):
		"""Calculates the value of a Bond object using continuous compounding"""
		return(sum(self.present_value_fcf_c()))

	def duration(self):
		"""Calculates the duration of a Bond object using daily compounding"""
		years_to_payments = [days / 365 for days in self.days_to_payments()]
		intermediate_dur_calcs = [(cf[0] * cf[1]) for cf in zip(self.present_value_fcf(), years_to_payments)]
		#bond_duration = sum(intermediate_dur_calcs)/self.value()
		#mm_duration = bond_duration/(1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)
		return sum(intermediate_dur_calcs)/self.value()

	def duration_c(self):
		"""Calculates the duration of a Bond object using continuous compounding"""
		years_to_payments = [days / 365 for days in self.days_to_payments()]
		intermediate_dur_calcs = [(cf[0] * cf[1]) for cf in zip(self.present_value_fcf_c(), years_to_payments)]
		return sum(intermediate_dur_calcs)/self.value_c()

	def modified_duration(self):
		"""Calculates the modified duration of a Bond object using daily compounding"""
		return self.duration()/(1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)

	def modified_duration_c(self):
		"""Calculates the modified duration of a Bond object using continuous compounding"""
		return self.duration_c()/(1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)

	def convexity(self):
		"""Calculates the convexity of an indivudal bond using daily compounding"""
		years_to_payments = [days / 365 for days in self.days_to_payments()]
		intermediate_conv_calcs = [((pv_cf[0])*(pv_cf[1]**2+pv_cf[1])) 
			for pv_cf in zip(self.present_value_fcf(),years_to_payments)]
		return (sum(intermediate_conv_calcs) / 
			(self.value() * (1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)**2))

	def convexity_c(self):
		"""Calculates the convexity of an indivudal bond using continuous compounding"""
		years_to_payments = [days / 365 for days in self.days_to_payments()]
		intermediate_conv_calcs = [((pv_cf[0])*(pv_cf[1]**2+pv_cf[1])) 
			for pv_cf in zip(self.present_value_fcf_c(),years_to_payments)]
		return (sum(intermediate_conv_calcs) / 
			(self.value_c() * (1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)**2))
		



if __name__ == "__main__":
	bond1 = Bond(face_value = 10000.0,
				maturity_date = '2022-06-15',
				coupon_rate = 2.5,
				payments_per_year = 2,
				rating = 'AAA',
				btype = 'Corporate')
	print(bond1.value())
	print(bond1.value_c())
	print((bond1.value_c()/bond1.value())*100)

	print(bond1.duration())
	print(bond1.duration_c())
	print((bond1.duration_c()/bond1.duration())*100)

	print(bond1.convexity())
	print(bond1.convexity_c())
	print((bond1.convexity_c()/bond1.convexity())*100)

	"""
	print(bond1.face_value)
	print(bond1.maturity_date)
	print(bond1.coupon_rate)
	print(bond1.payments_per_year)
	print(bond1.rating)
	print(bond1.btype)
	"""
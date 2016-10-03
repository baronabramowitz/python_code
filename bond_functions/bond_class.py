import date_functions as df
import BankDate_ as BD

class Bond(object):
	def __init__(self, face_value,maturity_date,coupon_rate,payments_per_year,rating,btype):
		self.face_value = face_value
		self.maturity_date = maturity_date
		self.coupon_rate = coupon_rate
		self.payments_per_year = payments_per_year
		self.rating = rating
		self.btype = btype

	def days_to_payments(self):
		payment_step = str(self.payments_per_year/12) + 'm'
		days_to_payments = df.days_to_payment(self.maturity_date,payment_step)
		return	days_to_payments

	def update_rating(self, new_rating):
		self.rating = new_rating

	def rating_premium(self):
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
		payment_step = str(self.payments_per_year/12) + 'm'
		discount_rates = df.yields_for_payment_dates(df.payment_dates(self.maturity_date, payment_step))
		return discount_rates

	def maturity_remaining(self):
		return (BD.BankDate().nbr_of_days(self.maturity_date))/365

	def coupon_payment(self):
		if self.payments_per_year == 0:
			coupon_payment = 0
		else:
			coupon_payment = ((self.coupon_rate/100)*self.face_value)/self.payments_per_year
		return coupon_payment

	def present_value_fcf(self):
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
	        
	   
	def value(self):
		return sum(self.present_value_fcf())

	def duration(self):
		"""Calculates the duration of a Bond object"""
		years_to_payments = [days / 365 for days in self.days_to_payments()]
		intermediate_dur_calcs = [(cf[0] * cf[1]) for cf in zip(self.present_value_fcf(), years_to_payments)]
		bond_duration = sum(intermediate_dur_calcs)/self.value()
		mm_duration = bond_duration/(1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)
		return {'Bond Duration' : bond_duration, 'Modified Duration' : mm_duration}

	def convexity(self):
		"""Calculates the convexity of an indivudal bond"""
		years_to_payments = [days / 365 for days in self.days_to_payments()]
		#cfs = list(zip(self.present_value_fcf(),years_to_payments))
		intermediate_conv_calcs = [((pv_cf[0])*(pv_cf[1]**2+pv_cf[1])) 
			for pv_cf in zip(self.present_value_fcf(),years_to_payments)]
		bond_convexity = (sum(intermediate_conv_calcs) / 
			(self.value() * (1 + sum(self.discount_rates())/len(self.discount_rates()) / 100)**2))
		return {'Bond Convexity':bond_convexity}
		



if __name__ == "__main__":
	bond1 = Bond(face_value = 10000.0,
				maturity_date = '2022-06-15',
				coupon_rate = 2.5,
				payments_per_year = 2,
				rating = 'AAA',
				btype = 'Corporate')

	print(bond1.convexity())

	"""
	print(bond1.face_value)
	print(bond1.maturity_date)
	print(bond1.coupon_rate)
	print(bond1.payments_per_year)
	print(bond1.rating)
	print(bond1.btype)
	"""
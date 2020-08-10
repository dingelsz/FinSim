from .security import Securities
from .wallstreet import get


class Market:
	""" Market is an interface for requesting financial data"""
	
	def __init__(self):
		self._securities = Securities()
		self._time = None
		
	def load(self, symbol):
		if symbol not in self._securities:
			self._securities.merge(
				securities = get(symbol,
				outputsize='full')
			)
		
	def get_current(self, symbol):
		self.load(symbol)
		return self._securities.get(symbol).get_date(self._time)
		
	@property
	def dates(self):
		return self._securities.dates
		
		
			
			

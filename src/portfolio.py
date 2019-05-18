from collections import Counter
from warnings import warn

from .wallstreet import get


class Portfolio:
	""" Portfolio is a class that represents a collection of assets and their quantity"""
	
	def __init__(self, initial_value):
		self._portfolio = Counter()
		self._portfolio['cash'] = initial_value
		
	def get(self, sec_id):
		return self._portfolio[sec_id]
		
	@property
	def cash(self):
		return self._portfolio['cash']
		
	@property
	def portfolio(self):
		return self._portfolio.copy()
		
	def _buy(self, symbol, price, quantity):
		if self.cash < price * quantity:
			warn(f'Attempting to spend more '
					 f'money than a portfolio has.')
		self._portfolio['cash'] -= price*quantity
		self._portfolio[symbol] += quantity
		
	def _sell(self, symbol, price, quantity):
		if self._portfolio[symbol] < quantity:
			raise PortfolioError('A portfolio cant sell more securities than it holds')
		self._portfolio['cash'] += price*quantity
		self._portfolio[symbol] -= quantity
		
	def __iter__(self):
		return iter(self._portfolio)
		
	def __repr__(self):
		return repr(self._portfolio)
		

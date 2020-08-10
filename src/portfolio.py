from collections import Counter
from warnings import warn

from .wallstreet import get


class PortfolioError(Exception): pass


class Portfolio:
	""" Portfolio is a class that represents a collection of assets and their quantity"""
	
	def __init__(self, initial_value):
		self._portfolio = Counter()
		self._portfolio['cash'] = initial_value
		self._initial_value = initial_value
		self._history = []
		
	def get(self, sec_id):
		return self._portfolio[sec_id]
		
	def copy(self):
		copy = Portfolio(self._initial_value)
		copy._portfolio = self._portfolio
		copy._history = self._history
		return copy
		
	@property
	def initial_value(self):
		return self._initial_value
		
	@property
	def cash(self):
		return self._portfolio['cash']
		
	@property
	def portfolio(self):
		return self._portfolio.copy()
		
	def _buy(self, symbol, price, quantity):
		total = price * quantity
		if total - self.cash > .1:
			raise PortfolioError(f'Attempting to spend more money than a portfolio has.')
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
		

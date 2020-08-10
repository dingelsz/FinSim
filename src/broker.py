
class Broker:
	"""A Broker object manages portfolios"""
	
	def __init__(self, market):
		self._portfolios = {}
		self._market = market
		self._transactions = []
		
	def add(self, id, portfolio):
		self._portfolios[id] = portfolio
		
	def get(self, id):
		return self._portfolios[id].copy()
		
	def order(self, portfolio, symbol, quantity):
		self._transactions.append((portfolio, symbol, quantity))
		
	def sell(self, portfolio, symbol, quantity, date):
		self.order(portfolio, symbol, -quantity)
		
	def _complete_transactions(self, date):
		for info in self._transactions:
			portfolio, symbol, quantity = info
			sec = self._market.get_current(symbol)
			price = sec.data.close
			portfolio._buy(symbol, price, quantity)
		
	def quote(self, symbol):
		sec = self._market.get_current(symbol)
		return sec.data.close
		
	def __iter__(self):
		return iter(self._portfolios)
	
	# Helper Functions	
	def calc_value(self, portfolio, date):
		total = 0
		for sec_id in portfolio:
			sec_amount = portfolio.get(sec_id)
			if sec_id == 'cash':
				total += sec_amount
			else:
				security = self._market.get_current(sec_id)
				sec_value = security.data.close
				total += sec_value * sec_amount
		return total
			
			
			

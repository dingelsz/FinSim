
class Broker:
	"""A Broker object manages portfolios"""
	
	def __init__(self, market):
		self._portfolios = {}
		self._market = market
		
	def add(self, id, portfolio):
		self._portfolios[id] = portfolio
		
	def get(self, id):
		return self._portfolios[id].copy()
		
	def buy(self, id, symbol, quantity):
		portfolio = self.get(id)
		price = self.market.get[symbol]
		portfolio._buy(symbol, price, quantity)
		
	def sell(self, id, symbol, quantity):
		portfolio = self.get(id)
		price = self.market.get[symbol]
		portfolio._sell(symbol, price, quantity)	
		
	# Helper Functions	
	def calc_value(portfolio, securities):
		total = 0
		for sec_id in portfolio:
			sec_amount = portfolio.get(sec_id)
			if sec_id == 'cash':
				total += sec_amount
			else:
				security = securities.get(sec_id)
				current = security.current_data
				sec_value = current.data.open
				total += sec_value * sec_amount
		return total
			
			
			

class DB:
	""" An interface to the local DB"""
	
	def __contains__(self, symbol):
		""" True if the symbol is in the DB and up to date"""
		pass
		
	def fetch(self, symbol):
		

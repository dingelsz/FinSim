class WallStreet:
	""" WallStreet is a class that serves securities data"""
	
	def get(symbol):
		if not symbol in DB:
			self.fetch(symbol)
		
		# Load from DB
		

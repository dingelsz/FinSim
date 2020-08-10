import requests as r


class API:
	
	url_base = ''
	
	def _build_url(self, **kargs):
		query_str = '&'.join([
			f'{key}={val}' 
			for key, val in kargs.items()
		])
		return f'{self.url_base}?{query_str}'
		
	def request(self, **kargs):
		url = self._build_url(**kargs)
		return r.get(url)
		
class AVAPI(API):
	url_base = 'https://www.alphavantage.co/query'
	
	def get_symbol(self, symbol):
		query = {
			'symbol': symbol,
			'datatype': 'csv',
			'function': 'TIME_SERIES_DAILY',
			'symbol': 'SPY',
			'outputsize': 'full',
			'datatype': 'json',
			'apikey': 'JPIO2GNGBMFRLGMN'
		}
		
		req = self.request(**query)
		
		# Reverse dates to past to present
		text = req.text
		header, *text = text.split()
		text = '\n'.join(
			[l for l in text[::-1]]
		)
		csv_str = f'{header}\n{text}'
		return csv_str

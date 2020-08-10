import requests as r

from .security import Security, Securities
from .data import Data


url_base = 'https://www.alphavantage.co/query'

def _build_url(**kargs):
	query = {
	'function': 'TIME_SERIES_DAILY',
	'symbol': 'SPY',
	'outputsize': 'full',
	'datatype': 'json',
	'apikey': 'JPIO2GNGBMFRLGMN'
	}
	query.update(kargs)
	
	query_str = '&'.join([f'{key}={val}' for key, val in query.items()])
	return f'{url_base}?{query_str}'
	
def _request(**kargs):
	url = _build_url(**kargs)
	return r.get(url)

def _get_symbol(symbol, **kargs):
	kargs['symbol'] = symbol
	kargs['datatype'] = 'csv'
	req = _request(**kargs)
	# Reverse dates to past to present
	text = req.text
	header, *text = text.split()
	text = '\n'.join(
		[l for l in text[::-1]]
	)
	csv_str = f'{header}\n{text}'

	data = Data.load_csv(csv_str)
	return Security(symbol, data) 
	
def get(symbols, **kargs):
	if not isinstance(symbols, list):
		symbols = [symbols]
		
	result = Securities()
	for symbol in symbols:
		kargs['symbol'] = symbol
		result.add(
			id=symbol,
			security=_get_symbol(**kargs)
		)
	return result
	

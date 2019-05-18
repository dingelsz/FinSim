import requests as r

from .security import Security, Securities
from .data import Data


url_base = 'https://www.alphavantage.co/query'

def _build_url(**kargs):
	query = {
	'function': 'TIME_SERIES_DAILY',
	'symbol': 'SPY',
	'outputsize': 'compact',
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
	data = Data.load_csv(req.text)
	return Security(symbol, data) 
	
def get(symbols, **kargs):
	if not isinstance(symbols, list):
		symbols = [symbols]
		
	result = Securities()
	for symbol in symbols:
		kargs['symbol'] = symbol
		result.add(_get_symbol(**kargs))
	return result
	
	
	
	
	
	
	
	
def _parse_data(data):
	# Parse the data into a matrix
	data = data['Time Series (Daily)']
	
	# Parse data into columns - by date
	dates = sorted(list(data.keys()))
	tmp = defaultdict(list)
	for date in dates:
		tmp['date'].append(date)
		for col_full in data[date]:
			col_name = col_full.split()[-1]
			info = data[date][col_full]
			info = float(info)
			tmp[col_name].append(info)
			
	tmp = {k: np.array(tmp[k]) for k in tmp}
	
	tmp['date'] = tmp['date'].astypet(np.datetime64).astype(datetime)
	return tmp

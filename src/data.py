from types import SimpleNamespace
from collections import defaultdict

import numpy as np

class DataError(Exception): pass

class Data:
	""" Data is an object that stores an indexed matrix"""
	
	def load_table(table, columns):
		data = Data()
		data._col_index = {col:i for i, col in enumerate(columns)}
		data._table = table
		return data
	
	def load_csv(csv_string, index=None):
		rows = csv_string.splitlines()
		table = [row.split(',') for row in rows]
		header, *table = table
		table = np.array(table)
		return Data.load_table(table, header)
		
	def __init__(self):
		self.__dict__['_col_index'] = {}
		self._table = {}
		self._columns = None
		
	@property
	def values(self):
		return self._table.copy()
		
	@property
	def columns(self):
		if self._columns is None:
			# sort cols for index
			tmp = [(v, k)
			for k, v in self._col_index.items()]
			tmp = sorted(tmp)
			self._columns = [col for (i, col) in tmp]
			
		return self._columns
		
	@property
	def shape(self):
		return self._table.shape
	
	def __rshift__(self, func):
		self = func(self)
		
	def _get_col(self, col):
		j = self._col_index[col]
		if len(self._table.shape) == 1:
			result = self._table[j]
		if len(self._table.shape) == 2:
			result = self._table[:, j]

		if col != 'timestamp':
			result = result.astype(float)
			if len(result) == 1:
				result = result[0]
		return result
		
	def _set_col(self, col, value):
		j = self._col_index[col]
		self._table[:, j] = value
		
	def __getitem__(self, key):
		if key not in self._col_index:
			raise DataError(f'Data does not contain key: {key}')
		return self._get_col(key)
		
	def __setitem__(self, key, value):
		if key in self._col_index:
			self._set_col(key, value)
		
	def __getattr__(self, attr):
		if attr in self._col_index:
			return self._get_col(attr)
		raise AttributeError(f'Data does not have attribute: {attr}')
		
	def __setattr__(self, attr, value):
		if attr in self._col_index:
			self._set_col(attr, value)
		else:
			self.__dict__[attr] = value

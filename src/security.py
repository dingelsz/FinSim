import numpy as np
from datetime import datetime
from collections import namedtuple

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from .data import Data


class Security:
	""" A security represents a uniquely identifiable and immutable object who's quantities have changed over time. """
		
	
	def __init__(self, id, data):
		self._id = id
		self._data = data
		self._dates = data.timestamp.astype(np.datetime64).astype(datetime)
		self._idates = {date: i for i, date in enumerate(self._dates)}
		
	@property
	def id(self):
		return self._id
	
	@property
	def data(self):
		return self._data
		
	@property
	def dates(self):
		return self._dates

	def __hash__(self):
		return hash(self._id)
		
	def __eq__(self, other):
		return self._id == other._id
		
	def __repr__(self):
		return f'Security: {self.id} - {self._data.shape}'
		
	def get_date(self, date, default=None):
		if date not in self._idates:
			return default
			
		i = self._idates[date]
		row = self._data._table[i:i+1,]
		data = Data.load_table(row, self.data.columns)
		return Security(self.id, data)
		
	@property
	def current_data(self):
		date = max(self.dates)
		return self.get_date(date)
	
	@property
	def oldest_data(self):
		date = min(self.dates)
		return self.get_date(date)
		
	def plot(self, column):
		X = self.dates
		Y = self.data[column]
		
		fig, ax = plt.subplots()
		fig.set_size_inches(20, 8)
		
		ax.plot(X, Y, 'b')
		
		myFmt = DateFormatter("%Y")
		ax.xaxis.set_major_formatter(myFmt)
		
		plt.show()
		
class SecuritiesError(Exception): pass

		
class Securities:
	""" Securities is a container for multiple Security objects"""
	
	def __init__(self):
		self._collection = {}
		self._dates = []
		
	def add(self, securities):
		if not isinstance(securities, list):
			securities = [securities]
		
		for s in securities:
			self._collection[s.id] = s
			self._dates.extend(s.dates)
			self._dates = sorted(list(set(self._dates)))
		
	def get(self, id):
		if id not in self._collection:
			raise SecuritiesError(f'Securities doesnt contain {id}')
		return self._collection[id]
		
	def get_date(self, date):
		result = Securities()
		for sec in self._collection.values():
			result.add(sec.get_date(date))
		return result
		
	@property
	def dates(self):
		return self._dates
		
	def __iter__(self):
		return iter(self._collection.keys())
		
	def __repr__(self):
		return f'Securities: {list(iter(self))}'
			
		

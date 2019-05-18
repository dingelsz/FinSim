class BaseClock:

	def __init__(self):
		self._time = None
		self._time_end = None
		self._time_step = None
		
	@property
	def time(self):
		assert self._time is not None, 'no time provided'
		return self._time
		
	@property
	def time_end(self):
		assert self._time_end is not None, 'no time end provided'
		return self._time_end
		
	@property
	def time_step(self):
		assert self._time_step is not None, 'no time step provided'
		return self._time_step
		
	def step_forward(self):
		self._time += self._time_step
		
	def step_backward(self):
		self._time -= self._time_step
		
	def copy(self):
		copy = BaseClock()
		copy._time = self._time
		copy._time_end = self._time_end
		copy._time_step = self._time_step
		return copy
		
	def __repr__(self):
		return f'time: {self._time}, step: {self._time_step}, end:{self._time_end}'
		
class DateClock(BaseClock):
	
	def __init__(self, time, time_end, time_step):
		self._time = time
		self._time_end = time_end
		self._time_step = time_step
		
class IterClock(BaseClock):
	def __init__(self, iter):
		self._time = 0
		self._time_end = len(iter)
		self._time_step = 1
		self._times = list(iter)
		
	@property
	def time(self):
		return self._times[self._time]
		
	@property
	def times(self):
		return self._times.copy()
		
	def is_active(self):
		return -1 < self._time and self._time < self._time_end
		
	def copy(self):
		copy = IterClock(self._times)
		copy._time = self._time
		return copy
		
	def __repr__(self):
		if not self.is_active():
			return f'inactive'
		return super().__repr__()
	


from types import SimpleNamespace

from .clock import IterClock
from .broker import Broker


class StateError: Exception


class State(SimpleNamespace):
	"""A class representing state as a namespace"""
	
	def copy(self):
		return State(**self.__dict__)
	
	def update(self, other):
		if not isinstance(other, State):
			raise StateError(f'Cannot update state with an object of type {type(other)}')
			self.__dict__.update(other.__dict__)


class ContextError(Exception): pass


class Context:
	"""A base class representing the context that a discrete, time bases process is running in"""
	
	def __init__(self):
		self._clock = None
		self._state = State()
		
	def setup(self, clock, initial_state, process):
		if not isinstance(clock, IterClock):
			raise ContextError(f'Context was passed in a {type(clock)} instead of an IterClock')
		self._clock = clock
		self._state = initial_state
		self._process = process
	
	@property
	def clock(self):
		return self._clock.copy()
		
	@property
	def state(self):
		return self._state.copy()
		
	def run(self):
		if self._clock is None:
			raise ContextError('Context must be provides a clock before running')
			
		while self._clock.is_active():
			self.step()
			self._clock.step_forward()
		return True
		
	def step(self):
		processed_step = self._process(self._state)
		if not isinstance(processed_step, State):
			raise ContextError('Provided process function must return a State')
			
		self._state.update(
			processed_step
		)
		
	def __repr__(self):
		if self._clock is None or self._state is None:
			return f'Context. Not setup'
		return f'Context. time: {self._clock}'
		
		
class HiddenContextError(Exception): pass
		
		
class HiddenContext(Context):
	""" An InnerContext is a context with a hidden state that allows the context to react to changes in state. It is an abstract class."""		
	
	def __init__(self):
		super().__init__()
		self._hidden_state = State()
		
	def _pre_step(self):
		raise HiddenContextError('_pre_step has not been implemented')
		
	def _post_step(self):
		raise HiddenContextError('_post_step has not been implemented')
		
	def step(self):
		self._pre_step()
		super().step()
		self._post_step()
		

class SecurityContext(HiddenContext):
	
	def __init__(self, securities, process, **kargs):
		self._securities = securities
		self._market = {}
		self._broker = Broker(self._market)
		state = State(**kargs)
		state.broker = self._broker
		
		self.setup(
			clock = IterClock(securities.dates),
			initial_state = state, 
			process = process
		)
		
	def _pre_step(self):
		self._broker._market = self._securities.get_date(self._clock.time)
		
	def _post_step(self):
		portfolio = self._state.portfolio.portfolio
		sec = self._securities.get_date(
			self._clock.time
		)
		value = Broker.calc_value(
			portfolio, sec
		)
		self._state.portfolio_history.append(
			(portfolio, value)
		)
			
		

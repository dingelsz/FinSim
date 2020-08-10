import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from src.context import SecurityContext
from src.broker import Broker
from src.portfolio import Portfolio
from src.wallstreet import get


def step(state):
	broker = state.broker
	portfolio = broker.get('zach')
	spy = broker.get('spy')
	
	if portfolio.cash > broker.quote('aapl'):
		broker.order(portfolio, 'aapl', 1)
		
	if spy.cash != 0:
		val = broker.quote('spy')
		broker.order(spy, 'spy', spy.cash / val)
	
	return state
	
simulation = SecurityContext(
	step, 
	# these go in state
	portfolios = {
		'zach': Portfolio(1000),
		'spy':  Portfolio(1000)
		}
)

simulation.run()


dates = simulation.clock.times
zach = simulation.state.broker.get('zach')._history
spy = simulation.state.broker.get('spy')._history

fig, ax = plt.subplots()
fig.set_size_inches(20, 8)

ax.plot(dates, spy, 'b')
ax.plot(dates, zach, 'r')

myFmt = DateFormatter("%Y")
ax.xaxis.set_major_formatter(myFmt)

plt.legend(['SPY', 'Zach'])

plt.show()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from src.context import SecurityContext
from src.broker import Broker
from src.portfolio import Portfolio
from src.wallstreet import get

securities = get(['spy', 'cost'], outputsize='full')

def step(state):
	broker = state.broker
	portfolio = brok
	
	
	return state
	
simulation = SecurityContext(
	securities, 
	step, 
	portfolio = Portfolio(1000),
	portfolio_history = []
)

simulation.run()


dates = simulation.clock.times
history = [val for s, val in simulation.state.portfolio_history]

fig, ax = plt.subplots()
fig.set_size_inches(20, 8)

ax.plot(dates, history, 'b')

myFmt = DateFormatter("%Y")
ax.xaxis.set_major_formatter(myFmt)

plt.show()

from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from src import WallStreet as WS

from src.processing import rolling_average


# Load data
securities = WS.get('SPY', )
spy = securities.get('SPY')

# process data
duration = 99

Y = spy.data.close.astype(float)
X = spy.dates

Y = np.log(Y)
Y = np.diff(Y, 1)
Y_90 = rolling_average(Y, 90)
Y_30 = rolling_average(Y, 30)

X =       X[-duration:]
Y_90 = Y_90[-duration:]
Y_30 = Y_30[-duration:]


# View
fig, ax = plt.subplots()
fig.set_size_inches(20, 8)

ax.plot(X, Y_90, 'b')
ax.plot(X, Y_30, 'r')

myFmt = DateFormatter("%Y")
ax.xaxis.set_major_formatter(myFmt)

plt.show()


from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

from src import wallstreet as WS

from src.processing import rolling_average

from io import BytesIO
import ui, appex


# Load data
symbol = 'MSFT'
securities = WS.get(symbol, )
spy = securities.get(symbol)

# process data
duration = 252

Y = spy.data.close.astype(float)
X = spy.dates

Y = np.log(Y)
Y = np.diff(Y, 1)
Y_90 = rolling_average(Y, 90)
Y_30 = rolling_average(Y, 30)

X    = X   [-duration:]
Y    = Y   [-duration:]
Y_90 = Y_90[-duration:]
Y_30 = Y_30[-duration:]


# View
fig, ax = plt.subplots()
fig.set_size_inches(40, 20)

ax.plot(X, [0] * len(X), 'black')

ax.plot(X, Y,    'gray', linewidth=1, alpha=.5)
ax.plot(X, Y_90, 'cyan', linewidth=5, alpha=.9)
ax.plot(X, Y_30, 'dodgerblue', linewidth=5, alpha=.9)

plt.legend(('Baseline', 'Actual', '30 RA', '90 RA'))

myFmt = DateFormatter("%M-%Y")
ax.xaxis.set_major_formatter(myFmt)

plt.show()

"""
b = BytesIO()
plt.savefig(b)
img = ui.Image.from_data(b.getvalue())

img_view = ui.ImageView(background_color='white')
img_view.content_mode = ui.CONTENT_SCALE_ASPECT_FIT
img_view.image = img
appex.set_widget_view(img_view)
#img_view.present()
"""

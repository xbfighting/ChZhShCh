import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from pandas import Series, DataFrame
from matplotlib.pylab import date2num

x = np.linspace(-3, 3, 50)
y1 = 2*x + 1
y2 = x**2

print(y1)
print(y2)
plt.figure()
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(y1, y2)
plt.show()
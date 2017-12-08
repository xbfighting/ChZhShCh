import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from pandas import Series, DataFrame
from matplotlib.pylab import date2num
# %matplotlib inline

ser = Series(np.random.randn(24))

print(ser)

ser[:8].plot(color='red')
ser[7:16].plot(color='green')
ser[15:24].plot(color='blue')
plt.show()
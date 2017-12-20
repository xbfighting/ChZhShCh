import numpy as np
from scipy import interpolate

x = np.arange(0,10)
y = np.exp(-x/3.0)
f = interpolate.interp1d(x, y)

xnew = np.arange(0,9,0.1)
import matplotlib.pyplot as plt
plt.plot(x,y,'o',xnew,f(xnew),'-')
plt.show()
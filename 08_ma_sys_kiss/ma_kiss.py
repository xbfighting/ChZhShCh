import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(r"../01_tushare")
import tushare_helper as th
sys.path.append(r"../02_candel_standardized")
import standardized as standard
sys.path.append(r"../09_show")
import show



original = th.TushareHelper('002500', datetime.date.today()+ datetime.timedelta(days=-30),datetime.date.today(),'60min')
original.data_transfer_ma()


x = original.data_frame_ma_mini['index']
y1 = original.data_frame_ma_mini['short']
y2 = original.data_frame_ma_mini['long']

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure()

plt.title("ma")
plt.xlabel("date")
plt.ylabel("price")

plt.plot(x, y1, color='red', linewidth=1.0, label="short")
plt.plot(x, y2, color='black', linewidth=1.0, label="long")
plt.legend()  # 展示图例
plt.show()


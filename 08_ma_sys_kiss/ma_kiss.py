import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sys.path.append(r"../01_tushare")
import tushare_helper as th
sys.path.append(r"../02_candel_standardized")
import standardized as standard
sys.path.append(r"../09_show")
import show

code = "002500"

original = th.TushareHelper(code, datetime.date.today()+ datetime.timedelta(days=-30),datetime.date.today(),'30min')
original.data_transfer_ma()

x_date = original.data_frame_ma_mini['index_date']
x = original.data_frame_ma_mini['index']
y1 = original.data_frame_ma_mini['short']
y2 = original.data_frame_ma_mini['long']

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# x 轴转换
# xtickers 表示
def date_tickers_transfer(data, xtickers):
    x_date = data['index_date']
    x = data['index']
    date_tickers = []
    # 时间轴转换
    for i in xtickers:
        index = int(i)
        if index == 0:
            date_tickers.append(x_date[int(i)])
        else:
            date_tickers.append(x_date[int(i) - 1])
    return date_tickers


xtickers = np.linspace(0, len(x), 5)
date_tickers = date_tickers_transfer(original.data_frame_ma_mini, xtickers)

plt.figure()

plt.title("ma")
plt.xlabel("date")
plt.ylabel("price")

plt.plot(x, y1, color='red', linewidth=1.0, label="short")
plt.plot(x, y2, color='black', linewidth=1.0, label="long")
plt.legend()  # 展示图例
plt.show()


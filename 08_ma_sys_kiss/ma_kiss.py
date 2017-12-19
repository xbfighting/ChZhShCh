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

original = th.TushareHelper(code, datetime.date.today()+ datetime.timedelta(days=-30),datetime.date.today(),'60min')
original.data_transfer_ma()

x_date = original.data_frame_ma_mini['index_date']
x = original.data_frame_ma_mini['index']
y1 = original.data_frame_ma_mini['short']
y2 = original.data_frame_ma_mini['long']

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

fig, ax = plt.subplots(1, 1, sharex=True)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

ax.plot(x, y1, color='red', linewidth=1.0, label="short")
ax.plot(x, y2, color='black', linewidth=1.0, label="long")
ax.fill_between(x, y1, y2, color='gray', alpha=0.2)
# ax.fill_between(x, y1, y2, where=y2 < 10, color='yellow', alpha=0.2)
# ax.fill_between(x, y1, y2, where=y2 < y1, facecolor='red', interpolate=True)

ax.set_title(code)
ax.set_xlabel("date-日期")
ax.set_ylabel("price")

plt.xticks(xtickers)
plt.xticks(xtickers, date_tickers)
ax.legend()  # 展示图例
plt.show()


# 画焦点 http://www.voidcn.com/article/p-gbgftgpm-bnu.html






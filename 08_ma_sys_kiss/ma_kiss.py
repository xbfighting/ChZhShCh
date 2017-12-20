import sys
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import interpolate

sys.path.append(r"../01_tushare")
import tushare_helper as th
sys.path.append(r"../02_candel_standardized")
import standardized as standard
sys.path.append(r"../09_show")
import show

class MAKiss(object):

    # x 轴转换 xtickers 表示
    def __date_tickers_transfer(self):
        self.date_tickers = []
        # 时间轴转换
        for i in self.int_tickers:
            index = int(i)
            if index == 0:
                self.date_tickers.append(self.x_date[int(i)])
            else:
                self.date_tickers.append(self.x_date[int(i) - 1])
        return self.date_tickers

    def __init__(self, code, data_frame_ma_mini):
        self.code = code
        self.data_frame_ma_mini = data_frame_ma_mini
        self.x_date = self.data_frame_ma_mini['index_date']
        self.x_index = self.data_frame_ma_mini['index']
        self.long = self.data_frame_ma_mini['long']
        self.short = self.data_frame_ma_mini['short']
        self.intersections = []
        self.intersections_ex = []
        self.int_tickers =  np.linspace(0, len(self.x_index), 5)
        self.date_tickers = self.__date_tickers_transfer()



# code = "002500"
#
# original = th.TushareHelper(code, datetime.date.today()+ datetime.timedelta(days=-30),datetime.date.today(),'60min')
# original.data_transfer_ma()
#
# x_date = original.data_frame_ma_mini['index_date']
# x = original.data_frame_ma_mini['index']
# y1 = original.data_frame_ma_mini['short']
# y2 = original.data_frame_ma_mini['long']
#
# f1 = interpolate.interp1d(x, y1)
# f2 = interpolate.interp1d(x, y2)
#
# x0 = np.linspace(0, x[len(x)-1], 10000)
# jd = np.where(f1(x0)- f2(x0) == 0)[0]
#
# # x 轴转换
# # xtickers 表示
# def date_tickers_transfer(data, xtickers):
#     x_date = data['index_date']
#     x = data['index']
#     date_tickers = []
#     # 时间轴转换
#     for i in xtickers:
#         index = int(i)
#         if index == 0:
#             date_tickers.append(x_date[int(i)])
#         else:
#             date_tickers.append(x_date[int(i) - 1])
#     return date_tickers
#
# xtickers = np.linspace(0, len(x), 5)
# date_tickers = date_tickers_transfer(original.data_frame_ma_mini, xtickers)
#
# fig, ax = plt.subplots(1, 1, sharex=True)
#
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
#
# ax.plot(x, y1, color='red', linewidth=1.0, label="short")
# ax.plot(x, y2, color='black', linewidth=1.0, label="long")
# ax.fill_between(x, y1, y2, color='gray', alpha=0.2)
# # ax.fill_between(x, y1, y2, where=y2 < 10, color='yellow', alpha=0.2)
# # ax.fill_between(x, y1, y2, where=y2 < y1, facecolor='red', interpolate=True)
#
# ax.set_title(code)
# ax.set_xlabel("date-日期")
# ax.set_ylabel("price")
#
# plt.xticks(xtickers)
# plt.xticks(xtickers, date_tickers)
# ax.legend()  # 展示图例
# plt.show()


# 画焦点 http://www.voidcn.com/article/p-gbgftgpm-bnu.html






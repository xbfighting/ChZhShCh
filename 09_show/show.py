import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import numpy as np
from pandas import Series, DataFrame
# http://blog.csdn.net/xiaodongxiexie/article/details/53123371

class PlotShow(object):

    def __init__(self, date_tickers, title):
        self.date_tickers = date_tickers
        self.xaxis_cycle = 30
        self.width = 0.3
        self.colordown ='#53c156'
        self.colorup = '#ff1717'
        self.xlabel = 'datetime'
        self.ylabel = 'value'
        self.title = title


    # 时间轴转换
    def __format_date(self, x, pos=None):
        if x < 0 or x > len(self.date_tickers) - 1:
            return ''
        return self.date_tickers[int(x)]

    # K画图
    def candle_show(self, stock_data, top_bottom_data):

        # 创建子图
        fig, ax = plt.subplots(figsize=(192.0 / 72, 108.0 / 72))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xaxis_cycle))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.__format_date))
        mpf.candlestick_ohlc(ax, stock_data, width=self.width, colordown=self.colordown, colorup=self.colorup, alpha=1)

        # title 各种设置
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # 顶底、图例等
        if len(top_bottom_data) > 0:
            x = []
            y = []
            for i in top_bottom_data:
                x.append(i[0])
                y.append(i[1])
            plt.plot(x, y, '--y*', label='分笔')
            plt.legend()  # 展示图例

        ax.grid(True)
        # plt.savefig('E:\PythonChZhShCh\\' + code + k_type + start_date + end_date + '.png')
        plt.show()

    # MA 画图
    def ma_kiss_show(self, ma):
        fig, ax = plt.subplots(1, 1, figsize=(192.0 / 72, 108.0 / 72), sharex=True)

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        ax.plot(ma.x_index, ma.short, color='red', linewidth=1.0, label="short")
        ax.plot(ma.x_index, ma.long, color='black', linewidth=1.0, label="long")
        # ax.fill_between(ma.x_index, ma.short, ma.long, color='gray', alpha=0.2)
        # ax.fill_between(x, y1, y2, where=y2 < 10, color='yellow', alpha=0.2)
        # ax.fill_between(x, y1, y2, where=y2 < y1, facecolor='red', interpolate=True)
        ax.plot(ma.intersection_x, ma.intersection_y, 'o')

        ax.set_title(self.title)
        ax.set_xlabel("日期")
        ax.set_ylabel("price")

        plt.xticks(ma.int_tickers)
        plt.xticks(ma.int_tickers, ma.date_tickers)
        ax.legend()
        plt.show()

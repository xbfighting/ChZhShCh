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
        self.ylabel = 'index value'
        self.title = title


    # 时间轴转换
    def __format_date(self, x, pos=None):
        if x < 0 or x > len(self.date_tickers) - 1:
            return ''
        return self.date_tickers[int(x)]

    # 画图
    def candle_show(self, stock_data, top_bottom_data):
        # TODO title 各种设置
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # 创建子图
        fig, ax = plt.subplots(figsize=(1920 / 72, 1080 / 72))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xaxis_cycle))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.__format_date))
        mpf.candlestick_ohlc(ax, stock_data, width=self.width, colordown=self.colordown, colorup=self.colorup, alpha=1)

        # TODO 顶底 Series
        ser = Series(1000 * np.abs(np.random.randn(60)))
        print(ser)
        # ser[:8].plot(color='red')
        # ser[7:16].plot(color='green')
        # ser[15:24].plot(color='blue')

        # TODO 图例等
        if len(top_bottom_data) > 0:
            x = []
            y = []
            for i in top_bottom_data:
                x.append(i[0])
                y.append(i[1])
            plt.plot(x, y, '--y*', label='bi')
            plt.legend()  # 展示图例

        ax.grid(True)
        # plt.savefig('E:\PythonChZhShCh\\' + code + k_type + start_date + end_date + '.png')
        plt.show()
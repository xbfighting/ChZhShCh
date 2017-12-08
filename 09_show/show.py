import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

class PlotShow(object):

    def __init__(self, date_tickers):
        self.date_tickers = date_tickers
        self.xaxis_cycle = 30
        self.width = 0.3
        self.colordown ='#53c156'
        self.colorup = '#ff1717'

    # 时间轴转换
    def __format_date(self, x, pos=None):
        if x < 0 or x > len(self.date_tickers) - 1:
            return ''
        return self.date_tickers[int(x)]

    # 画图
    def candle_show(self, stock_data, top_bottom_data=[]):
        # 创建子图
        fig, ax = plt.subplots(figsize=(192.0 / 72, 108.0 / 72))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xaxis_cycle))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.__format_date))

        mpf.candlestick_ohlc(ax, stock_data, width=self.width, colordown=self.colordown, colorup=self.colorup, alpha=1)
        ax.grid(True)
        plt.show()
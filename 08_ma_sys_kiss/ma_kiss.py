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





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
        self.long_interp1d = interpolate.interp1d(self.x_index, self.long)
        self.short_interp1d = interpolate.interp1d(self.x_index, self.short)
        self.intersection = {'Postural': '', 'X': 0, 'Y': 0}
        self.intersections = []
        self.intersections_ex = []
        self.int_tickers =  np.linspace(0, len(self.x_index), 5)
        self.date_tickers = self.__date_tickers_transfer()
        self.postural_long_to_short = "1"
        self.postural_short_to_long = "0"


    def __get_intersection(self, pre_data, curr_data):
        pre_short = pre_data["short"]
        pre_long = pre_data["long"]
        curr_short = curr_data["short"]
        curr_long = curr_data["long"]

        if np.isnan(pre_short) != True and np.isnan(pre_long) != True and np.isnan(curr_short) != True and np.isnan(curr_long) != True:
            if pre_long - pre_short > 0 and curr_short - curr_long >= 0:
                intersection_index = (curr_data["index"] + pre_data["index"]) / 2
                y = self.long_interp1d(intersection_index)
                if np.isnan(y):
                    y = self.short_interp1d(intersection_index)
                self.intersection = {'Postural': self.postural_long_to_short, 'X': intersection_index, 'Y': y}
                self.intersections.append(self.intersection)

            if pre_long - pre_short < 0 and curr_short - curr_long <= 0:
                intersection_index = (curr_data["index"] + pre_data["index"]) / 2
                y = self.long_interp1d(intersection_index)
                if np.isnan(y):
                    y = self.short_interp1d(intersection_index)
                self.intersection = {'Postural': self.postural_short_to_long, 'X': intersection_index, 'Y': y}
                self.intersections.append(self.intersection)
        pass
    def get_intersections(self):
        pass

# f1 = interpolate.interp1d(x, y1)
# f2 = interpolate.interp1d(x, y2)


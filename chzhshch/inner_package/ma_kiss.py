import os
import sys
import datetime
import math

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from scipy import interpolate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))

from external_package import line_helper as lh
from external_package import tushare_helper as th
from inner_package import standardized as standard
from inner_package import show


class MAKiss(object):
    # x 轴转换 date_tickers 表示
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
        self.data_frame_ma_mini = data_frame_ma_mini  # ma 数据
        self.x_date = self.data_frame_ma_mini['index_date']  # x轴用日期
        self.x_index = self.data_frame_ma_mini['index']  # x轴用数字索引
        self.long = self.data_frame_ma_mini['long']  # 长期均线
        self.short = self.data_frame_ma_mini['short']  # 短期均线
        self.long_interp1d = interpolate.interp1d(self.x_index, self.long)  # 长期均线差值函数
        self.short_interp1d = interpolate.interp1d(self.x_index, self.short)  # 短期均线差值函数
        self.intersection = {"Postural": None, "X": 0, "Y": 0}  # 交点定义
        self.intersections = []  # 交点集合
        self.intersections_ex = []  # 交点集合 ex 备用计算吻之用
        self.intersection_x = []  # 交点x点集
        self.intersection_y = []    # 交点y点集

        self.lip_kiss = []  # 唇吻集合
        self.lip_kiss_x = []    # 唇吻 x点集
        self.lip_kiss_y = []    # 唇吻 y点集


        self.int_tickers = np.linspace(0, len(self.x_index), 5)  # plot int tickers
        self.date_tickers = self.__date_tickers_transfer()  # plot date tickers

        self.postural_long_to_short = "1"  # 男上位
        self.postural_short_to_long = "0"  # 女上位

    # 单个交点计算和获取 粗略版 已经弃用
    def __get_intersection(self, pre_data, curr_data):
        pre_short = pre_data["short"]
        pre_long = pre_data["long"]
        curr_short = curr_data["short"]
        curr_long = curr_data["long"]

        # 空缺值不处理
        if np.isnan(pre_short) != True and np.isnan(pre_long) != True and np.isnan(curr_short) != True and np.isnan(
                curr_long) != True:
            # 交点前是男上位
            if pre_long - pre_short > 0 and curr_short - curr_long >= 0:
                intersection_index = (curr_data["index"] + pre_data["index"]) / 2
                y = self.long_interp1d(intersection_index)
                if np.isnan(y):
                    y = self.short_interp1d(intersection_index)
                self.intersection = {"Postural": self.postural_long_to_short, "X": intersection_index, "Y": y}
                return
            # 交点前是女上位
            if pre_long - pre_short < 0 and curr_short - curr_long <= 0:
                intersection_index = (curr_data["index"] + pre_data["index"]) / 2
                y = self.long_interp1d(intersection_index)
                if np.isnan(y):
                    y = self.short_interp1d(intersection_index)
                self.intersection = {"Postural": self.postural_short_to_long, "X": intersection_index, "Y": y}
                return

        self.intersection = {"Postural": None, "X": 0, "Y": 0}
        return

    # 单个交点计算和获取 ex
    def __get_intersection_ex(self, pre_data, curr_data):
        pre_short = pre_data["short"]
        pre_long = pre_data["long"]
        pre_index = pre_data["index"]
        curr_short = curr_data["short"]
        curr_long = curr_data["long"]
        curr_index = curr_data["index"]

        # 空缺值不处理
        if np.isnan(pre_short) != True and np.isnan(pre_long) != True and np.isnan(curr_short) != True and np.isnan(
                curr_long) != True:
            # 交点前是男上位
            if pre_long - pre_short > 0 and curr_short - curr_long >= 0:
                point_long1 = lh.Point(pre_index, pre_long)
                point_long2 = lh.Point(curr_index, curr_long)
                line1_long = lh.Line(point_long1, point_long2)

                point_short1 = lh.Point(pre_index, pre_short)
                point_short2 = lh.Point(curr_index, curr_short)
                line1_short = lh.Line(point_short1, point_short2)

                intersection_point = lh.GetCrossPoint(line1_long, line1_short)
                self.intersection = {"Postural": self.postural_long_to_short, "X": intersection_point.x,
                                     "Y": intersection_point.y}
                return
            # 交点前是女上位
            if pre_long - pre_short < 0 and curr_short - curr_long <= 0:
                point_long1 = lh.Point(pre_index, pre_long)
                point_long2 = lh.Point(curr_index, curr_long)
                line1_long = lh.Line(point_long1, point_long2)

                point_short1 = lh.Point(pre_index, pre_short)
                point_short2 = lh.Point(curr_index, curr_short)
                line1_short = lh.Line(point_short1, point_short2)

                intersection_point = lh.GetCrossPoint(line1_long, line1_short)
                self.intersection = {"Postural": self.postural_short_to_long, "X": intersection_point.x,
                                     "Y": intersection_point.y}
                return

        self.intersection = {"Postural": None, "X": 0, "Y": 0}
        return


    # 交点集合获取
    def get_intersections(self):
        i = 1
        while i < len(self.data_frame_ma_mini["index"]):
            ma_item_pre = {'index': 0, 'long': 0, 'short': 0}
            ma_item_pre["index"] = self.data_frame_ma_mini["index"][i - 1]
            ma_item_pre["long"] = self.data_frame_ma_mini["long"][i - 1]
            ma_item_pre["short"] = self.data_frame_ma_mini["short"][i - 1]

            ma_item_curr = {'index': 0, 'long': 0, 'short': 0}
            ma_item_curr["index"] = self.data_frame_ma_mini["index"][i]
            ma_item_curr["long"] = self.data_frame_ma_mini["long"][i]
            ma_item_curr["short"] = self.data_frame_ma_mini["short"][i]

            self.__get_intersection_ex(ma_item_pre, ma_item_curr)

            if self.intersection["Postural"] is not None:
                self.intersections.append(self.intersection)
                self.intersection_x.append(self.intersection["X"])
                self.intersection_y.append(self.intersection["Y"])
            i += 1

    # 获取唇吻
    # TODO: 排除交点附近的点
    # TODO: 想办法获取两个交点中断的“吻”

    def get_lip_kiss(self):
        long_short_diff = []
        long_short_diff_value = []

        for i in range(len(self.x_index)):
            if np.isnan(self.long[i]) != True and np.isnan(self.short[i]) != True:
                diff = self.long[i] - self.short[i]
                if diff > 0:
                    long_short_diff.append({"Postural": self.postural_long_to_short, "X": self.x_index[i], "Y":self.long[i], "Diff": round(diff, 5)})
                    long_short_diff_value.append(round(diff, 5))

        for passnum in range(len(long_short_diff_value) - 1, 0, -1):
            for i in range(passnum):
                if long_short_diff[i]["Diff"] > long_short_diff[i + 1]["Diff"]:
                    temp = long_short_diff[i]
                    long_short_diff[i] = long_short_diff[i + 1]
                    long_short_diff[i + 1] = temp
        print(long_short_diff)
        for i in range(len(long_short_diff)):
            if i < 8:
                self.lip_kiss.append(long_short_diff[i])
                self.lip_kiss_x.append(long_short_diff[i]["X"])
                self.lip_kiss_y.append(long_short_diff[i]["Y"])
        print(long_short_diff)

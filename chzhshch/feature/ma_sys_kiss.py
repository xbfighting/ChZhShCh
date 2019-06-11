# -*- coding: UTF-8 -*-
# 均线系统+吻
import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
from external_package import tushare_helper as th
from inner_package import standardized as standard
from inner_package import show
from inner_package import ma_kiss as mk

code = "002500"
original = th.TushareHelper(code, datetime.date.today() + datetime.timedelta(days=-30), datetime.date.today() + datetime.timedelta(days=1),'60min')
original.data_transfer_ma()

makiss = mk.MAKiss(code, original.data_frame_ma_mini)
my_plot = show.PlotShow([], code)

# 交点获取
makiss.get_intersections()
print(len(makiss.intersections))
print(makiss.intersections)

# 吻获取
makiss.get_lip_kiss()
print(makiss.lip_kiss)

# 打印
my_plot.ma_kiss_show(makiss)



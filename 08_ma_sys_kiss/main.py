import sys
import datetime
sys.path.append(r"../01_tushare")
import tushare_helper as th
sys.path.append(r"../02_candel_standardized")
import standardized as standard
sys.path.append(r"../09_show")
import show
sys.path.append(r"../08_ma_sys_kiss")
import ma_kiss as mk

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



import sys

import datetime

sys.path.append(r"00_common")
sys.path.append(r"01_tushare")
import tushare_helper as th
sys.path.append(r"02_candel_standardized")
import standardized as standard
sys.path.append(r"09_show")
import show

# original = th.TushareHelper('000001', datetime.date.today()+ datetime.timedelta(days=-1),datetime.date.today() + datetime.timedelta(days=+1),'1min')
original = th.TushareHelper('000001', '2017-12-04', '2017-12-12','D')
original.data_transfer()

sta = standard.StandardHandle(original.data_original)
sta.deal_candle()
sta.get_top_bottom()

# date_tickers = original.date_tickers
# my_plot = show.PlotShow(date_tickers, '000001上海')
# my_plot.candle_show(original.data_original_ex, [])

date_tickers = sta.date_tickers
my_plot = show.PlotShow(date_tickers, '000001')
# my_plot.candle_show(sta.standardized_list_ex, [])
my_plot.candle_show(sta.standardized_list_ex, sta.top_bottom_list_ex)
my_plot.candle_show(sta.standardized_list_ex, sta.standardized_top_bottom_list_ex)


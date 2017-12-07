import sys
sys.path.append(r"00_common")
sys.path.append(r"01_tushare")
import tushare_helper as th
sys.path.append(r"02_candel_standardized")
import standardized as standard

import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.finance as mpf

original = th.TushareHelper('000001', '2017-12-01','2017-12-04','30min')
original.data_transfer()
print(len(original.data_original))

sta = standard.StandardHandle(original.data_original)
sta.deal_candle()
print(len(sta.standardized_list_ex))

# for item in test.data_original:
#     print(item)

# for item in test.data_original_ex:
#     print(item)

# for i in sta.standardized_list:
#     print (i)




date_tickers = []
## 时间轴转换
def format_date(x, pos=None):
    if x<0 or x>len(date_tickers)-1:
        return ''
    return date_tickers[int(x)]

## 画图
def candle_show(stock_data, xaxis_cycle):
    # 创建子图
    fig, ax = plt.subplots(figsize=(200 / 72, 48 / 72))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(xaxis_cycle))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

    mpf.candlestick_ohlc(ax, stock_data, width=0.3, colordown='#53c156', colorup='#ff1717', alpha=1)
    ax.grid(True)
    plt.show()

date_tickers = original.date_tickers
candle_show(original.data_original_ex, 60)

date_tickers = sta.date_tickers
candle_show(sta.standardized_list_ex, 60)


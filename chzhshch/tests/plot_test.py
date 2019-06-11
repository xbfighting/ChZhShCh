# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.finance as mpf


def candle_show(self, stock_data, scatter_data):
    # 创建子图
    fig, ax = plt.subplots(figsize=(192.0 / 72, 108.0 / 72))
    mpf.candlestick_ohlc(ax, stock_data, width=self.width, colordown=self.colordown, colorup=self.colorup, alpha=1)
    ax.grid(True)
    plt.show()

plt.title('0000001')
plt.xlabel('datetime')
plt.ylabel('index value')

arr = [	[0, 3316.95],	[1, 3304.58],	[2, 3313.19],	[3, 3303.01]]
x = []
y = []
for i in arr:
    x.append(i[0])
    y.append(i[1])

plt.plot(x, y, '--y*', label = 'bi')
plt.legend() # 展示图例
plt.show()
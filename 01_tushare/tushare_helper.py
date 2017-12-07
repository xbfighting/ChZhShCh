import tushare as ts
from datetime import datetime, date, time

# 单例
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


class TushareConn(Singleton):
    conn = ts.get_apis()

class TushareHelper(object):
    def __init__(self, code, start, end, freq, asset=''):
        self.self = self
        self.code = code
        self.start = start
        self.end = end
        self.freq = freq
        if asset is None or asset == '':
            self.asset = 'INDEX'
        else:
            self.asset = asset

        self.data_frame = {}
        self.data_original = []
        self.data_original_ex = []
        self.date_tickers = []

    def __bar(self):
        self.data_frame = ts.bar(code=self.code, conn=TushareConn.conn, start_date=self.start, end_date=self.end,
                                 freq=self.freq, asset=self.asset)
    def data_transfer(self):
        self.__bar()
        list_index = 0
        # data_frame 按照 index 倒叙排序
        for index, row in self.data_frame.sort_index().iterrows():
            date_time = datetime.strptime(str(index), '%Y-%m-%d %H:%M:%S')
            row["index"] = str(date_time)
            row["is_up"] = row["open"] <= row["close"]
            self.data_original_ex.append((list_index, row['open'], row['high'], row['low'], row['close']))
            self.data_original.append(row)
            self.date_tickers.append(str(row['index']))
            list_index += 1

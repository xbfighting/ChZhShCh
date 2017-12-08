import sys
sys.path.append(r"../00_common")
import frequency_enum as fe
sys.path.append(r"../01_tushare")
import tushare_helper as th

class StandardHandle(object):
    def __init__(self, original_list):
        self.candle_direction = 0
        self.is_merged = False
        # 原始列表初始化标准列表
        self.standardized_list = original_list
        self.standardized_list_ex=[]
        self.date_tickers = []
    # 方向
    def __set_direction(self, item_pre, item_curr):
        high_pre = item_pre['high']
        low_pre = item_pre['low']
        high_curr = item_curr['high']
        low_curr = item_curr['low']
        if high_curr > high_pre and low_curr > low_pre:
            self.candle_direction = 1
        elif high_pre > high_curr and low_pre > low_curr:
            self.candle_direction = -1

    # 合并
    def __merge_candles(self, item_pre, item_curr):
        result = []
        high_pre = item_pre['high']
        low_pre = item_pre['low']
        high_curr = item_curr['high']
        low_curr = item_curr['low']
        is_up_pre = item_pre['is_up']
        is_up_curr = item_curr['is_up']

        if high_curr >= high_pre and low_curr <= low_pre:
            if self.candle_direction == 1:
                item_curr['low'] = low_pre
                item_pre['high'] = high_curr

                if is_up_curr:
                    item_curr['open'] = low_pre
                else:
                    item_curr['close'] = low_pre

                if is_up_pre:
                    item_pre['close'] = high_curr
                else:
                    item_pre['open'] = high_curr

                self.is_merged = True
            elif self.candle_direction == -1:
                item_curr['high'] = high_pre
                item_pre['low'] = low_curr

                if is_up_curr:
                    item_curr['close'] = high_pre
                else:
                    item_curr['open'] = high_pre

                if is_up_pre:
                    item_pre['open'] = low_curr
                else:
                    item_pre['close'] = low_curr

                self.is_merged = True
            else:
                self.is_merged = False
        elif high_pre >= high_curr and low_pre <= low_curr:
            if self.candle_direction == 1:
                item_curr['high'] = high_pre
                item_pre['low'] = low_curr

                if is_up_curr:
                    item_curr['close'] = high_pre
                else:
                    item_curr['open'] = high_pre

                if is_up_pre:
                    item_pre['open'] = low_curr
                else:
                    item_pre['close'] = low_curr

                self.is_merged = True
            elif self.candle_direction == -1:
                item_curr['low'] = low_pre
                item_pre['high'] = high_pre

                if is_up_curr:
                    item_curr['open'] = low_pre
                else:
                    item_curr['close'] = low_pre

                if is_up_pre:
                    item_pre['close'] = high_curr
                else:
                    item_pre['open'] = high_curr

                self.is_merged = True
            else:
                self.is_merged = False
        else:
            self.is_merged = False

        result.append(item_curr)
        result.append(item_pre)
        return result

    # 标准化处理
    def deal_candle(self):
        i = 0
        while i < len(self.standardized_list):
            item_curr = self.standardized_list[i]
            if i > 0:
                item_pre = self.standardized_list[i - 1]
                self.__set_direction(item_pre, item_curr)
                item_curr_pre = self.__merge_candles(item_pre, item_curr)
                if self.is_merged:
                    self.standardized_list[i] = item_curr_pre[0]
                    self.standardized_list.pop(i - 1)
                    i -= 1
            i += 1

        list_index = 0
        for row in self.standardized_list:
            self.date_tickers.append(str(row['index']))
            self.standardized_list_ex.append((list_index, row['open'], row['high'], row['low'], row['close']))
            list_index += 1
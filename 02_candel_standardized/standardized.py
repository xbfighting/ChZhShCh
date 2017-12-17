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
        self.standardized_list_ex = []
        self.top_bottom_list = [] #普通顶底
        self.top_bottom_list_ex = [] #普通顶底ex
        self.standardized_top_bottom_list_temp = []  # 标准顶底 temp
        self.standardized_top_bottom_list = [] #标准顶底
        self.standardized_top_bottom_list_ex = [] #标准顶底ex
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

    # 获取分型类型
    def __get_typing(self, pre, curr, after):
        high_pre = pre['high']
        high_curr = curr['high']
        high_after = after['high']

        typing = 0 # 0-无顶底，1-顶分型，-1-底分型
        direction = 0 # 方向类型

        if high_curr > high_pre:
            direction = 1
            typing = 1
        else:
            direction = -1
            typing = -1

        if high_after < high_curr:
            direction = direction - 1
        else:
            direction = direction + 1

        if direction == 0:
            return typing
        else:
            return 0

    # 思路
    # 1、先获取所有的顶和底，标准转向
    # 2、连续顶底的处理
    # 3、输出

    # 获取顶和底
    def get_top_bottom(self):
        s_length = len(self.standardized_list)
        typing = 0

        i = 0
        while i < s_length:
            if i > 0 and s_length - i > 1:
                pre = self.standardized_list[i - 1]
                curr = self.standardized_list[i]
                after = self.standardized_list[i + 1]
                typing = self.__get_typing(pre, curr, after)
                if typing != 0:
                    curr["int_index"] = i
                    curr["typing"] = typing
                    if typing == 1:
                        curr["typing_value"] = curr["high"]
                    else:
                        curr["typing_value"] = curr["low"]
                    self.top_bottom_list.append(curr)
                    self.standardized_top_bottom_list.append(curr)
            i += 1

        print("top_bottom_list")
        print(len(self.top_bottom_list))

        for item in self.top_bottom_list:
            self.top_bottom_list_ex.append([item["int_index"], item["typing_value"]])
            print(item["int_index"], item["typing_value"], item["typing"])

        # 顶底不仅要考虑是否有3k，还需考虑分型区间是否包含 ！~！！！！！！
        # 连续顶顶或底底的情况要考虑极值的相比
        s_length = len(self.top_bottom_list)

        # 不成笔的区间 flag表示当前区间用作确认顶还是底
        # 顶=1 底=-1
        temp_rang = {"_top": None, "_bottom": None, "_flag":0}

        # 不足5k的顶底去除
        for i in range(0, s_length, 1):
            if s_length - i > 1:
                curr = self.top_bottom_list[i]
                after = self.top_bottom_list[i + 1]

                # 若不成笔区间不存在，则表示当前点和前面的点满足一笔且前点不存在争议
                if temp_rang["_top"] is None and temp_rang["_bottom"] is None:
                    if after["int_index"] - curr["int_index"] >= 4:
                        self.standardized_top_bottom_list_temp.append(curr)
                    else:
                        # 如果不成笔区间未初始化 则需要重新确认不成笔区间
                        if curr["typing"] == -1:
                            temp_rang["_top"] = after
                            temp_rang["_bottom"] = curr
                            temp_rang["_flag"] = -1

                        else:
                            temp_rang["_top"] = curr
                            temp_rang["_bottom"] = after
                            temp_rang["_flag"] = 1
                # 分型区间存在，表示当前点和前点不足一笔
                else:
                    # 确认底
                    if temp_rang["_flag"] == -1:
                        # 当前为顶
                        if curr["typing"] == 1:
                            # 当前和区间底构成一笔 则区间底确认，不够成一笔 不处理
                            if curr["int_index"] - temp_rang["_bottom"]["int_index"] >= 4:
                                self.standardized_top_bottom_list_temp.append(temp_rang["_bottom"])

                                if after["int_index"] - curr["int_index"] >= 4:
                                    self.standardized_top_bottom_list_temp.append(curr)
                                    # reset range
                                    temp_rang = {"_top": None, "_bottom": None, "_flag": 0}
                                else:
                                    # 判断笔破坏
                                    if after["typing_value"] < temp_rang["_bottom"]["typing_value"]:
                                        self.standardized_top_bottom_list_temp.pop(len(self.standardized_top_bottom_list_temp) - 1)
                                        self.standardized_top_bottom_list_temp.append(after)
                                        temp_rang = {"_top": None, "_bottom": None, "_flag": 0}
                                    else:
                                        # 新区间 确认顶
                                        temp_rang["_top"] = curr
                                        temp_rang["_bottom"] = after
                                        temp_rang["_flag"] = 1

                        # 当前为底
                        else:
                            # 比较底和区间底，如果较小则更新区间底，在区间内不处理
                            if curr["typing_value"] < temp_rang["_bottom"]["typing_value"]:
                                temp_rang["_bottom"] = curr

                    # 确认顶
                    else:
                        # 当前为顶
                        if curr["typing"] == 1:
                            # 比较顶和区间顶，如果较大则更新区间顶，在区间内不处理
                            if curr["typing_value"] > temp_rang["_top"]["typing_value"]:
                                temp_rang["_top"] = curr
                        # 当前为底
                        else:
                            # 当前和区间顶构成一笔 则区间顶确认，不够成一笔 不处理
                            if curr["int_index"] - temp_rang["_top"]["int_index"] >= 4:
                                self.standardized_top_bottom_list_temp.append(temp_rang["_top"])

                                if after["int_index"] - curr["int_index"] >= 4:
                                    self.standardized_top_bottom_list_temp.append(curr)
                                    # reset range
                                    temp_rang = {"_top": None, "_bottom": None, "_flag": 0}
                                else:
                                    # 判断笔破坏
                                    if after["typing_value"] > temp_rang["_top"]["typing_value"]:
                                        self.standardized_top_bottom_list_temp.pop(len(self.standardized_top_bottom_list_temp) - 1)
                                        self.standardized_top_bottom_list_temp.append(after)

                                        # reset range
                                        temp_rang = {"_top": None, "_bottom": None, "_flag": 0}
                                    else:
                                        # 新区间 确认底
                                        temp_rang["_top"] = after
                                        temp_rang["_bottom"] = curr
                                        temp_rang["_flag"] = -1

        print("standardized_top_bottom_list_temp")
        print(len(self.standardized_top_bottom_list_temp))
        # to simple series
        for item in self.standardized_top_bottom_list_temp :
            self.standardized_top_bottom_list_ex.append([item["int_index"], item["typing_value"]])
            print(item["int_index"], item["typing_value"], item["typing"])


import sys
import datetime
sys.path.append(r"../00_common")
import chzhshch_central as central

sys.path.append(r"../01_tushare")
import tushare_helper as th


class DailyClassfication(object):
    def __init__(self, original_list):
        # 原始列表初始化标准列表
        self.standardized_list = original_list
        pass

    # 中枢判断，如果是中枢则返回区间和高低点
    def is_central(self, k1, k2, k3):
        pass

    # 是否在中枢区间内
    def is_in_central_region(self, k, central):
        pass

    # 是否是预测，小于8K则属于预测
    def is_predict(self):
        if self.standardized_list is None or self.standardized_list.length < 8 :
            return True
        else:
            return False

    # 中枢个数
    def get_central_count(self):
        pass

    # 零个中枢
    def deal_zero_central(self):
        pass

    # 一个中枢
    def deal_one_central(self):
        pass

    # 两个中枢
    def deal_two_central(self):
        pass


original = th.TushareHelper('000001', datetime.date.today() + datetime.timedelta(days=-1),
                            datetime.date.today() + datetime.timedelta(days=+1), '30min')
original.data_transfer()

dcf = DailyClassfication(original.data_original)
print(dcf.standardized_list)

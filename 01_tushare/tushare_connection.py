import sys
import json
from datetime import datetime
#F:\GitHub\ChZhShCh_Python\00_common\__frequency_enum__\frequency_enum.py
#sys.path.append(r"F:\GitHub\ChZhShCh_Python\01_tushare")
#sys.path.append(r"")
import tushare_helper


# frequency_enum.
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

me = Object()
me.name = "Onur"
me.age = 35
me.dog = Object()
me.dog.name = "Apollo"
me.dog.create_date = str(datetime.now())

print(me.toJSON())
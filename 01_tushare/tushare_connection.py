import json

from datetime import datetime


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
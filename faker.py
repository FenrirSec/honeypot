import json
import re

class Faker():

    def __init__(self, filename):
        self.entries = {}
        data = json.load(open(filename))
        for key in data.keys():
            self.entries[re.compile(key)] = data[key]

    def handle(self, buf, data=None):
        print(buf)
        for re in self.entries.keys():
            out = re.search(buf)
            if out:
                if '%s' in self.entries[re]:
                   return self.entries[re] %out.group(1)
                return self.entries[re]

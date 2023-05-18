import json
import re

class Faker():

    def __init__(self, filename):
        self.entries = {}
        data = json.load(open(filename))
        for key in data.keys():
            if not key.startswith('0x'):
                self.entries[re.compile(key)] = data[key]
            else:
                self.entries[key] = data[key]

    def handle(self, buf, data=None):
        for re in self.entries.keys():
            if isinstance(re, str) and re.startswith('0x'):
                if re[2:] in data.hex():
                    return self.entries[re]
            else:
                out = re.search(buf)
                if out:
                    if '%s' in self.entries[re]:
                        return self.entries[re] %out.group(1)
                    return self.entries[re]

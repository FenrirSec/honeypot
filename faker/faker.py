import json
import re

def init(filename):
    e = {}
    data = json.load(open(filename))
    for k in data.keys():
        e[re.compile(k)] = data[k]
    return e

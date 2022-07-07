"""
Custom logger for honeypot
"""

import io
from datetime import datetime

class Logger():

    def __init__(self, dest):
        if type(dest) == io.TextIOWrapper:
            print('Logging into file', dest)

    def save(self):        
        return
    
    def log(self):
        return

    def warn(self):
        return

    def debug(self):
        return

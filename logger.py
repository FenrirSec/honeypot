"""
Custom logger for honeypot
"""


import io
from binascii import hexlify
from datetime import datetime

class Logger():

    def __init__(self, dest):
        if type(dest) == io.TextIOWrapper:
            print('Logging into file', dest)
        self.dest = dest

    def save(self, line):
        if type(self.dest) == io.TextIOWrapper:
            self.dest.write(line)

    def log(self, protocol, data, addr, level="log"):
        line = None
        try:
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol.name, protocol.port, addr.host, data.decode('UTF-8').replace(';', '%3B').replace('\n', '\\n').replace('\r', '\\r'))
        except Exception as e:
            print(e)
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol.name, protocol.port, addr,host, hexlify(data).decode('UTF-8'))
        print(line)
        self.save(line)

    def log_raw(self, protocol_name, protocol_port, client_ip, data, level="log"):
        line = None
        try:
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol_name, protocol_port, client_ip, data.decode('UTF-8').replace(';', '%3B').replace('\n', '\\n').replace('\r', '\\r'))
        except Exception as e:
            print(e)
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol_name, protocol_port, client_ip, hexlify(data).decode('UTF-8'))
        print(line)
        self.save(line)

    def warn(self, protocol, data, addr):
        self.log(protocol, data, addr, "warn")

    def debug(self, protocol, data, addr):
        self.log(protocol, data, addr, "debug")

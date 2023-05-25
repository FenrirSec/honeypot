"""
Custom logger for honeypot
"""

import io
import requests
from binascii import hexlify
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from conf import INGRESS_SERVER, INGRESS_SERVER_RSA_KEY, INGRESS_SERVER_HTTPS_CERT, DEBUG

BATCH_SIZE = 128

class Logger():

    def __init__(self, dest):
        if type(dest) == io.TextIOWrapper and DEBUG:
            print('Logging into file', dest)
        self.dest = dest

    def save(self, line):
        if type(self.dest) == io.TextIOWrapper:
            self.dest.write(line)
    
    def report_ingress_server(self, line):
        url = 'https://%s:5000/ingress' %INGRESS_SERVER

        with open(INGRESS_SERVER_RSA_KEY, 'r') as f:
            public_key = RSA.import_key(f.read())
       
        cipher = PKCS1_OAEP.new(public_key)

        message = []

        while len(line) > 0:
            block = cipher.encrypt(line[:BATCH_SIZE].encode('UTF-8')).hex()
            message.append(block)
            line = line[BATCH_SIZE:]

        response = requests.post(url, json=message, verify=INGRESS_SERVER_HTTPS_CERT)

        if DEBUG:
            print(response.status_code, response.text)

       
    def log(self, protocol, data, addr, level="log"):
        line = None
        try:
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol.name, protocol.port, addr.host, data.decode('UTF-8').replace(';', '%3B').replace('\n', '\\n').replace('\r', '\\r'))
        except Exception as e:
            if DEBUG:
                print(e)
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol.name, protocol.port, addr.host, hexlify(data).decode('UTF-8'))
        print(line)
        self.save(line)
        if INGRESS_SERVER:
            self.report_ingress_server(line)

    def log_raw(self, protocol_name, protocol_port, client_ip, data, level="log"):
        line = None
        try:
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol_name, protocol_port, client_ip, data.decode('UTF-8').replace(';', '%3B').replace('\n', '\\n').replace('\r', '\\r'))
        except Exception as e:
            if DEBUG:
                print(e)
            line = "%s;%s;%s;%s;%s;%s\n" %(level, datetime.now(), protocol_name, protocol_port, client_ip, hexlify(data).decode('UTF-8'))
        print(line)
        self.save(line)
        if INGRESS_SERVER:
            self.report_ingress_server(line)

    def warn(self, protocol, data, addr):
        self.log(protocol, data, addr, "warn")

    def debug(self, protocol, data, addr):
        self.log(protocol, data, addr, "debug")

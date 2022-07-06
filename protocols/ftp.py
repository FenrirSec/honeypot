from .protocol import Protocol
from faker import Faker
from datetime import datetime

BANNER= "220 (vsFTPd 2.3.4)\n"

def init(host):
    f = Faker('templates/ftp.json')
    p = Protocol('FTP', 21, host, f.handle, BANNER)
    p.listen()
    return p

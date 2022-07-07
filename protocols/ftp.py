from .protocol import Protocol
from faker import Faker
from datetime import datetime

BANNER= "220 (vsFTPd 2.3.4)\n"

def init(host, logger):
    f = Faker('templates/ftp.json')
    p = Protocol('FTP', 21, host, f.handle, logger, BANNER)
    p.listen()
    return p

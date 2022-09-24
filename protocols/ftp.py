from .TCPProtocol import * 
from faker import Faker

BANNER= "220 (vsFTPd 2.3.4)\n"

def init(host, logger):
    f = Faker('templates/ftp.json')
    factory = TCPProtocolFactory('FTP', 21, host, f.handle, logger, BANNER)
    p = factory.buildProtocol(host)
    p.listen()
    return p

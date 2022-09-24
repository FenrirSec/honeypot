from .TCPProtocol import *
from faker import Faker

BANNER= "+OK Dovecot Ready.\r\n"

def init(host, logger):
    f = Faker('templates/pop.json')
    factory = TCPProtocolFactory('POP', 110, host, f.handle, logger, BANNER)
    p = factory.buildProtocol(host)
    p.listen()
    return p

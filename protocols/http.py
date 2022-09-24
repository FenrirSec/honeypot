from .TCPProtocol import *
from faker import Faker

BANNER= None

def init(host, logger):
    f = Faker('templates/http.json')
    factory = TCPProtocolFactory('HTTP', 80, host, f.handle, logger, BANNER)
    p = factory.buildProtocol(host)
    p.listen()
    return p

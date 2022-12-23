
from .TCPProtocol import *
from twisted.internet import ssl, reactor
from faker import Faker

BANNER= None

def init(host, logger):
    f = Faker('templates/http.json')
    factory = TCPProtocolFactory('HTTPS', 8443, host, f.handle, logger, BANNER)
    factory.buildProtocol(host)
    return factory


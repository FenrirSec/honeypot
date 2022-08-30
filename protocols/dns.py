from asyncio import protocols
from .protocol import Protocol
from faker import Faker

BANNER = None

def init(host,logger):
    f = Faker('templates/dns.json')
    p = Protocol('DNS', 53 ,host, f.handle, logger,  BANNER)
    p.listen()
    return p
from .protocol import Protocol
from faker import Faker

BANNER= None

def init(host, logger):
    f = Faker('templates/http.json')
    p = Protocol('HTTP', 80, host, f.handle, logger, BANNER)
    p.listen()
    return p

from .protocol import Protocol
from faker import Faker

BANNER= None

def init(host):
    f = Faker('templates/http.json')
    p = Protocol('HTTP', 80, host, f.handle, BANNER)
    p.listen()
    return p

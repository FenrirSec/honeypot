from .protocol import Protocol
from faker import Faker
from datetime import datetime

BANNER= "+OK Dovecot Ready.\r\n"

def init(host):
    f = Faker('templates/pop.json')
    p = Protocol('POP', 110, host, f.handle, BANNER)
    p.listen()
    return p

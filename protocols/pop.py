from .protocol import Protocol
from faker import Faker
from datetime import datetime

BANNER= "+OK Dovecot Ready.\r\n"

def init(host, logger):
    f = Faker('templates/pop.json')
    p = Protocol('POP', 110, host, f.handle, logger, BANNER)
    p.listen()
    return p

from .TCPProtocol import *
from faker import Faker
from datetime import datetime

BANNER= "220-company.biz ESMTP #1 %s\n220-We do not authorize the user of this system to transport unsollicited,\n220 and/or bulk e-mail.\n" %datetime.now()

def init(host, logger):
    f = Faker('templates/smtp.json')
    factory = TCPProtocolFactory('SMTP', 25, host, f.handle, logger, BANNER)
    p = factory.buildProtocol(host)
    p.listen()
    return p

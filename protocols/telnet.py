from .TCPProtocol import TCPProtocol, TCPProtocolFactory
from faker import Faker

BANNER= """
********************************************************
* [WARNING] *
* This system is private. If you are not authorized *
* to access this system, exit immediately. *
* Unauthorized access to this system is forbidden by *
* company policies, national, and international laws. *
* Unauthorized users are subject to criminal and civil *
* penalties as well as company initiated disciplinary *
* proceedings. *
* *
* By entry into this system you acknowledge that you *
* are authorized access and the level of privilege you *
* subsequently execute on this system. You further *
* acknowledge that by entry into this system you *
* expect no privacy from monitoring. *
********************************************************

User Access Verification

Username: """


f = Faker('templates/telnet.json')

def init(host, logger):
    f = Faker('templates/telnet.json')
    factory = TCPProtocolFactory('Telnet', 23, host, f.handle, logger, BANNER)
    p = factory.buildProtocol(host)
    p.listen()

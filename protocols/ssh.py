from .protocol import Protocol
from faker import Faker
from datetime import datetime

BANNER= "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n"

def init(host):
    f = Faker('templates/ssh.json')
    p = Protocol('SSH', 22, host, f.handle, BANNER)
    p.listen()
    return p

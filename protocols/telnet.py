from .protocol import Protocol

def init(host):
    p = Protocol('Telnet', 23, host)
    p.listen()
    return p

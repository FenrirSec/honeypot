from .protocol import Protocol
from faker import faker

BANNER= """Welcom to Company's Telnet Server

User Access Verification

Username: """

f = None

def handler(buf):
    for re in f.keys():
        out = re.search(buf)
        print('Out', out)
        if out:
            print('Match', re, buf)
            if '%s' in f[re]:
                return f[re] %out.group(1)
            return f[re]

def init(host):
    global f
    p = Protocol('Telnet', 23, host, handler, BANNER)
    f = faker.init('templates/telnet.json')
    p.listen()
    return p

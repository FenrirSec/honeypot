from .protocol import Protocol
from faker import Faker

BANNER= "Android Debug Bridge (ADB):\n  Name: SM-G975N\n  Model: SM-G975N\n  Device: SM-G975N\n  Features:\n    cmd\n    shell_v2\n"

def init(host, logger):
    f = Faker('templates/adb.json')
    p = Protocol('adb', 5555, host, f.handle, logger, BANNER)
    p.listen()
    return p

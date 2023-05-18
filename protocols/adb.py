import struct
import codecs
import binascii
from .TCPProtocol import *
from faker import Faker

BANNER= """Android Debug Bridge (ADB):
    Name: rk322x_box
    Model: TV BOX
    Device: rk322x_box
    Features:
      sendrecv_v2_brotli
      remount_shell
      sendrecv_v2
      abb_exec
      fixed_push_mkdir
      fixed_push_symlink_timestamp
      abb
      shell_v2
      cmd
      ls_v2
      apex
      stat_v2
"""

def init(host, logger):
    f = Faker('templates/adb.json')
    factory = TCPProtocolFactory('adb', 5555, host, f.handle, logger, BANNER)
    p = factory.buildProtocol(host)
    p.listen()
    return p

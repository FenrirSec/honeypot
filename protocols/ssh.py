import sys

from zope.interface import implementer
from faker import Faker
from datetime import datetime
from twisted.internet import reactor
from twisted.conch.ssh import factory, keys, session
from twisted.conch.ssh.transport import SSHServerTransport
from twisted.conch.ssh import connection, factory, keys, session, userauth
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from twisted.conch.checkers import InMemorySSHKeyDB, SSHPublicKeyChecker
from twisted.python import components, log
from twisted.cred import portal
from twisted.conch.ssh.common import getNS
from twisted.cred import credentials
from twisted.conch import error, interfaces

## Implementation examples
## https://docs.twistedmatrix.com/en/stable/conch/examples/

PORT = 22
BANNER= "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n"

SERVER_RSA_PRIVATE = "keys/ssh_host_rsa_key"
SERVER_RSA_PUBLIC = "keys/ssh_host_rsa_key.pub"

PRIMES = { 2048: [(2,int("4217939"),)], 4096: [(2,int("4112035938859"),)], }

logger = None

log.startLogging(sys.stderr)

class AuthServer(userauth.SSHUserAuthServer):
    def auth_password(self, packet):
        if 'password' not in self.supportedAuthentications:
            self.supportedAuthentications.append(b'password')
        addr = self.transport.getPeer().address.host
        password = getNS(packet[1:])[0]
        logger.log_raw('SSH', PORT, addr, 'failed login with {} : {}'.format(self.user.decode('utf-8'), password.decode('utf-8')).encode('UTF-8'))
        c = credentials.UsernamePassword(self.user, password)
        return self.portal.login(c, None, interfaces.IConchUser)\
                          .addErrback(self._ebPassword)
      
    
@implementer(portal.IRealm)
class SSHRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        return super(self, avatarId, mind, interfaces)

class SSHFactory(factory.SSHFactory):
    protocol = SSHServerTransport

    services = {
        b"ssh-userauth": AuthServer,
        b"ssh-connection": connection.SSHConnection,
    }

    def __init__(self):
        users = {"admin":"admin123"}
        passwdDB = InMemoryUsernamePasswordDatabaseDontUse(**users)
        sshDB = SSHPublicKeyChecker(InMemorySSHKeyDB({b"user": []}))
        self.portal = portal.Portal(SSHRealm(), [passwdDB, sshDB])

    def getPublicKeys(self):
        return {b"ssh-rsa": keys.Key.fromFile(SERVER_RSA_PUBLIC)}

    def getPrivateKeys(self):
        return {b"ssh-rsa": keys.Key.fromFile(SERVER_RSA_PRIVATE)}

    def getPrimes(self):
        return PRIMES

def ssh_handler(data):    
    print(data)
    return f.handle(data)

def init(host, global_logger):
    global logger
    logger = global_logger
    f = Faker('templates/ssh.json')
    factory = SSHFactory()
    return reactor.listenTCP(PORT, factory)


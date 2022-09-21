import sys

from zope.interface import implementer
from .protocol import Protocol
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

log.startLogging(sys.stderr)

## Implementation examples
## https://docs.twistedmatrix.com/en/stable/conch/examples/

SERVER_RSA_PRIVATE = "keys/ssh_host_rsa_key"
SERVER_RSA_PUBLIC = "keys/ssh_host_rsa_key.pub"

PRIMES = {
    2048: [
        (
            2,
            int(
                "4217939"
            ),
        )
    ],
    4096: [
        (
            2,
            int(
                "4112035938859"
            ),
        )
    ],
}


BANNER= "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n"

@implementer(portal.IRealm)
class ExampleRealm:
    def requestAvatar(self, avatarId, mind, *interfaces):
        return super(self, avatarId, mind, interfaces)

class ExampleFactory(factory.SSHFactory):
    protocol = SSHServerTransport

    services = {
        b"ssh-userauth": userauth.SSHUserAuthServer,
        b"ssh-connection": connection.SSHConnection,
    }

    def __init__(self):
        passwdDB = InMemoryUsernamePasswordDatabaseDontUse(user="password")
        sshDB = SSHPublicKeyChecker(InMemorySSHKeyDB({b"user": []}))
        self.portal = portal.Portal(ExampleRealm(), [passwdDB, sshDB])

    def getPublicKeys(self):
        return {b"ssh-rsa": keys.Key.fromFile(SERVER_RSA_PUBLIC)}

    def getPrivateKeys(self):
        return {b"ssh-rsa": keys.Key.fromFile(SERVER_RSA_PRIVATE)}

    def getPrimes(self):
        return PRIMES

def ssh_handler(data):
    
    print(data)
    return f.handle(data)

def init(host, logger):
    f = Faker('templates/ssh.json')
    reactor.listenTCP(5022, ExampleFactory())

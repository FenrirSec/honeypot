import sys

from zope.interface import implementer
from faker import Faker
from datetime import datetime
from twisted.internet import reactor
from twisted.conch import avatar, recvline, interfaces as conchinterfaces
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
from twisted.conch.insults import insults

from faker import Faker

## Implementation examples
## https://docs.twistedmatrix.com/en/stable/conch/examples/

PORT = 22
BANNER = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\n"
HEADER = "Last login: Thu May 18 01:07:54 2023 from 80.215.234.158\n"
PS1 = "%s@vps$ "

SERVER_RSA_PRIVATE = "keys/ssh_host_rsa_key"
SERVER_RSA_PUBLIC = "keys/ssh_host_rsa_key.pub"

PRIMES = { 2048: [(2,int("4217939"),)], 4096: [(2,int("4112035938859"),)], } # Our main concern here is not the privacy of the fake accesses to the server

logger = None
f = None

log.startLogging(sys.stderr)

class AuthServer(userauth.SSHUserAuthServer):
    def auth_password(self, packet):
        if 'password' not in self.supportedAuthentications:
            self.supportedAuthentications.append(b'password')
        addr = self.transport.getPeer().address.host
        password = getNS(packet[1:])[0]
        logger.log_raw('SSH', PORT, addr, 'failed login with {} : {}'.format(self.user.decode('utf-8'), password.decode('utf-8')).encode('UTF-8'))
        c = credentials.UsernamePassword(self.user, password)
        login = self.portal.login(c, None, interfaces.IConchUser)\
                          .addErrback(self._ebPassword)
        return login


class FakeSSHProtocol(recvline.HistoricRecvLine):
    def __init__(self, user):
       self.user = user
 
    def connectionMade(self):
        recvline.HistoricRecvLine.connectionMade(self)
        self.terminal.write(HEADER)
        self.terminal.nextLine()
        self.showPrompt()
 
    def showPrompt(self):
        self.terminal.write(PS1 %self.user.user.decode('UTF-8'))
 
    def lineReceived(self, line):
        line = line.decode('UTF-8').strip()
        f.handle(line)
        self.terminal.write(f.handle(line))
        self.showPrompt()

@implementer(conchinterfaces.ISession)
class SSHAvatar(avatar.ConchUser):

    def __init__(self, user, prompt, commands):
        avatar.ConchUser.__init__(self)

        self.user = user
        self.prompt = prompt
        self.commands = commands
        self.channelLookup.update({b'session': session.SSHSession})

    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(FakeSSHProtocol, self)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, terminal, windowSize, attrs):
        return None

    def execCommand(self, protocol, cmd):
        pass

    def closed(self):
        pass

    def eofReceived(self):
        pass

    def windowChanged(self):
        pass
    
class SSHRealm:
    def __init__(self):
        self.prompt = HEADER
        self.commands = []

    def requestAvatar(self, avatarId, mind, *interfaces):
        if conchinterfaces.IConchUser in interfaces:
            return interfaces[0], SSHAvatar(avatarId, self.prompt,
                                            self.commands), lambda: None
        else:
            raise Exception("No supported interfaces found.")

class SSHFactory(factory.SSHFactory):
    protocol = SSHServerTransport

    services = {
        b"ssh-userauth": AuthServer,
        b"ssh-connection": connection.SSHConnection,
    }

    def __init__(self):
        users = {"admin": b"admin123", "root": b"password"}
        passwdDB = InMemoryUsernamePasswordDatabaseDontUse(**users)
        sshDB = SSHPublicKeyChecker(InMemorySSHKeyDB({b"user": []}))
        self.portal = portal.Portal(SSHRealm(), [passwdDB, sshDB])

    def getPublicKeys(self):
        return {b"ssh-rsa": keys.Key.fromFile(SERVER_RSA_PUBLIC)}

    def getPrivateKeys(self):
        return {b"ssh-rsa": keys.Key.fromFile(SERVER_RSA_PRIVATE)}

    def getPrimes(self):
        return PRIMES

def init(host, global_logger):
    global logger
    global f
    logger = global_logger
    f = Faker('templates/ssh.json')
    factory = SSHFactory()
    return reactor.listenTCP(PORT, factory)

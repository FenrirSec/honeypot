import codecs
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from binascii import hexlify


"""
TCP Protocol generic wrapper over Twisted protocols and factories
"""


class TCPProtocolFactory(Factory):
    def __init__(self, name, port, host, handler, logger, banner=None, buffer_size=1024):
        self.name = name
        self.port = port
        self.host = host
        self.handler = handler
        self.logger = logger
        self.banner = banner
        self.buffer_size = buffer_size

    def buildProtocol(self, addr):
        return TCPProtocol(self, self.name, self.port, self.host, self.handler, self.logger, self.banner, self.buffer_size)

class TCPProtocol(Protocol):
    def __init__(self, factory, name, port, host, handler, logger, banner=None, buffer_size=1024):
        self.factory = factory
        self.name = name
        self.port = port
        self.host = host
        self.clients = []
        self.banner = banner
        self.buffers = {}
        self.handler = handler
        self.logger = logger
        self.buffer_size = buffer_size

    def log(self, msg, level="LOG"):
        if level == "LOG":
            print("(LOG)[%s] %s" %(self.name, msg))
        if level == "DEBUG":
            print("(DEBUG)[%s] %s" %(self.name, msg))
                
    def dataReceived(self, data):
        self.log('Got data %s' %data)
        self.logger.log(self, data, self.transport.getPeer())
        host = self.transport.getPeer().host
        port = self.transport.getPeer().port
        if self.buffers[self.transport.getPeer()] is None:
            self.buffers[self.transport.getPeer()] = ""
        try:
            self.buffers[self.transport.getPeer()] += data.decode('UTF-8')
        except Exception as e:
            self.buffers[self.transport.getPeer()] += data.hex()
            print(e)
        buf = self.buffers[self.transport.getPeer()]
        answer = self.handler(buf, data)
        if answer:
            if isinstance(answer, str):
                self.buffers[self.transport.getPeer()] += answer
                if answer.startswith('0x'):
                    self.transport.write(codecs.decode(answer[2:], 'hex_codec'))
                else:
                    self.transport.write(answer.encode('UTF-8'))
            elif isinstance(answer, bytes):
                self.buffers[self.transport.getPeer()] += answer.hex()
                self.transport.write(answer)
            else:
                self.log('Unknown handler answer type : %s' %type(answer), DEBUG)
    
    def connectionMade(self):
        if self.banner:
            self.transport.write(self.banner.encode('UTF-8'))
        self.buffers[self.transport.getPeer()] = self.banner
        self.log('{} opened a connection'.format(self.transport.getPeer().host))

    def connectionLost(self, reason):
        if self.transport.getPeer() in self.buffers:
            del self.buffers[self.transport.getPeer()]
        self.log('{} closed the connection'.format(self.transport.getPeer().host))

    def listen(self):
        endpoint = TCP4ServerEndpoint(reactor, self.port)
        endpoint.listen(TCPProtocolFactory(self.name, self.port, self.host, self.handler, self.logger, self.banner, self.buffer_size))

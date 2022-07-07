import socket
from binascii import hexlify

class Protocol():
    def __init__(self, name, port, host, handler, logger, banner=None, buffer_size=1024):
        self.name = name
        self.port = port
        self.host = host
        self.buffer_size = buffer_size
        self.clients = []
        self.socket = None
        self.banner = banner
        self.buffers = {}
        self.handler = handler
        self.logger = logger

    def log(self, msg, level="LOG"):
        if level == "LOG":
            print("(LOG)[%s] %s" %(self.name, msg))
        if level == "DEBUG":
            print("(DEBUG)[%s] %s" %(self.name, msg))

    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.log("Listening on port %s" %self.port)

    def accept(self):
        if self.socket is not None:
            client, address = self.socket.accept()
            self.log('Got a connection from %s:%s' %address)
            if self.banner:
                client.send(self.banner.encode('UTF-8'))
            self.clients.append(client)
            self.buffers[client] = self.banner if self.banner else ""
                
    def read(self, c_sock):
        r = None
        try:
            r = c_sock.recv(self.buffer_size)
        except Exception as e:
            self.clients.remove(c_sock)
        if r:
            self.log('Got data %s' %r)
            self.logger.log(self, r, c_sock)
            if c_sock in self.buffers.keys():
                buf = self.buffers[c_sock]
                try:
                    self.buffers[c_sock] += r.decode('UTF-8')
                except Exception as e:
                    self.buffers[c_sock] += hexlify(r).decode('UTF-8')
                out = self.handler(self.buffers[c_sock])
                if out:
                    c_sock.send(out.encode('UTF-8'))
                    self.log('Answering %s' %out, "DEBUG")
                    self.buffers[c_sock] += out
    
    def handle_msg(self):
        return

    def get_read_sockets(self):
        return [self.socket] + self.clients

    def get_write_sockets(self):
        return [self.socket]

    def __del__(self):
        if self.socket:
            self.socket.close()

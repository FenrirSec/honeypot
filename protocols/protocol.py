import socket

class Protocol():
    def __init__(self, name, port, host, handler, banner=None, buffer_size=1024):
        self.name = name
        self.port = port
        self.host = host
        self.buffer_size = buffer_size
        self.clients = []
        self.socket = None
        self.banner = banner
        self.buffers = {}
        self.handler = handler

    def log(self, msg, level="LOG"):
        if level == "LOG":
            print("[%s] %s" %(self.name, msg))
        
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
        r = c_sock.recv(self.buffer_size)
        if r:
            self.log('Got data %s' %r)
            if c_sock in self.buffers.keys():
                buf = self.buffers[c_sock]
                self.log('Buffer is %s' %buf)
                self.buffers[c_sock] += r.decode('UTF-8')
                out = self.handler(self.buffers[c_sock])
                if out:
                    c_sock.send(out.encode('UTF-8'))
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

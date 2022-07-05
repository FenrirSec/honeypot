import socket

class Protocol():
    def __init__(self, name, port, host, buffer_size=1024):
        self.name = name
        self.port = port
        self.host = host
        self.buffer_size = buffer_size
        self.clients = []
        self.socket = None

    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print("%s is listening on port %s" %(self.name, self.port))

    def accept(self):
        if self.socket is not None:
            client, address = self.socket.accept()
            print('Got a connection from', address)
            self.clients.append(client)
                
    def read(self, c_sock):
        r = c_sock.recv(self.buffer_size)
        if r:
            print('Got data', r)
        
    def handle_msg(self):
        return

    def get_read_sockets(self):
        return [self.socket] + self.clients

    def get_write_sockets(self):
        return [self.socket]

    def __del__(self):
        if self.socket:
            self.socket.close()

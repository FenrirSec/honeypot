#!/usr/bin/env python3

from logger import Logger
from select import select
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from protocols import telnet, smtp, ssh, http, ftp, adb, pop

HOST=""
LOOP=True
logger = Logger(open("logs/log.txt", "a+"))
protos = []
sockets = []

def     loop():
    print(loop)
    r_sockets = []
    w_sockets = []
    e_sockets = []
    
    for p in protos:
        r_sockets = r_sockets + p.get_read_sockets()
        w_sockets = w_sockets + p.get_write_sockets()
    
    r, w, e = select(r_sockets, w_sockets, e_sockets)
    for sock in r:
        if sock.fileno() in sockets.keys():
            p = sockets[sock.fileno()]
            if sock.fileno() == p.socket.fileno():
                p.accept()
        else:
            for p in protos:
                if sock in p.clients:
                    p.read(sock)
    return

def	main():
    global protos
    global sockets
    sockets = {}
    # Twisted init
    ssh.init(HOST, logger)

    # Non-twisted init
    protos = [
        telnet.init(HOST, logger),
        smtp.init(HOST, logger),
        http.init(HOST, logger),
        ftp.init(HOST, logger),
        adb.init(HOST, logger),
        pop.init(HOST, logger)
    ]
    for p in protos:
        sockets[p.socket.fileno()] = p
    lc = LoopingCall(loop)
    lc.start(0.1)
    reactor.run()
    return 0

if __name__ == '__main__':
  exit(main())

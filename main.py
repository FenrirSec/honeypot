#!/usr/bin/env python3

from logger import Logger
from select import select
from protocols import telnet, smtp, ssh, http, ftp, adb, pop

HOST=""
LOOP=True
logger = Logger(open("logs/log.txt", "a+"))

def	main():
    sockets = {}
    protocols = [
        telnet.init(HOST),
        smtp.init(HOST),
        ssh.init(HOST),
        http.init(HOST),
        ftp.init(HOST),
        adb.init(HOST),
        pop.init(HOST)
    ]
    for p in protocols:
        sockets[p.socket.fileno()] = p

    while LOOP:
        r_sockets = []
        w_sockets = []
        e_sockets = []
        for p in protocols:
            r_sockets = r_sockets + p.get_read_sockets()
            w_sockets = w_sockets + p.get_write_sockets()
    
        r, w, e = select(r_sockets, w_sockets, e_sockets)
        for sock in r:
            if sock.fileno() in sockets.keys():
                p = sockets[sock.fileno()]
                if sock.fileno() == p.socket.fileno():
                    p.accept()
            else:
                for p in protocols:
                    if sock in p.clients:
                        p.read(sock)

    return 0

if __name__ == '__main__':
  exit(main())

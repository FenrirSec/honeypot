#!/usr/bin/env python3

from select import select
from protocols import telnet, smtp, ssh, http, ftp

HOST=""
LOOP=True

def	main():
    sockets = {}
    protocols = [
        telnet.init(""),
        smtp.init(""),
        ssh.init(""),
        http.init(""),
        ftp.init("")
    ]
    while LOOP:
        r_sockets = []
        w_sockets = []
        e_sockets = []
        
        for p in protocols:
            sockets = {p.socket: p}
            r_sockets = r_sockets + p.get_read_sockets()
            w_sockets = w_sockets + p.get_write_sockets()
    
        r, w, e = select(r_sockets, w_sockets, e_sockets)
        for sock in r:
            if sock in sockets.keys():
                p = sockets[sock]
                if sock is p.socket:
                    p.accept()
            else:
                for p in protocols:
                    if sock in p.clients:
                        p.read(sock)
    return 0

if __name__ == '__main__':
  exit(main())

#!/usr/bin/env python3

from logger import Logger
from twisted.internet import reactor
from protocols import telnet, smtp, ssh, http, ftp, adb, pop

HOST=""
logger = Logger(open("logs/log.txt", "a+"))

def	main():

    ssh.init(HOST, logger)
    telnet.init(HOST, logger)
    adb.init(HOST, logger)
    ftp.init(HOST, logger)
    http.init(HOST, logger)
    pop.init(HOST, logger)
    smtp.init(HOST, logger)
    
    reactor.run()
    
    return 0

if __name__ == '__main__':
  exit(main())

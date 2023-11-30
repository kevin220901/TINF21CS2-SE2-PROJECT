#!/usr/bin/python3

from server.logger import *
from sys import stdout
from server.server import Server


host = 'localhost'
port = 5555

logger.info(f'>>> starting blokus server on {host}:{port}')


server = Server(host, port, False)
server.start()

logger.info(f'<<< blokus server: waiting for connections')
#!/usr/bin/python3

import threading
from server.logger import *
from sys import stdout
from server.server import Server


host = '0.0.0.0'
port = 6666

stopEvent = threading.Event()

server = Server(host, port, stopEvent)


#this loop is required for the server to run in docker, 
#reason: 
#   Server starts its own thread for handling incomming clien requests
#   If the main thread is not occupied docker throws the error: could not create thread ...

#An alternativ solution could be returning the logic of the serverthread to the main thread. 
# Final conclusion on how to coop with this problem hast yet to be discussed (or not, lol)
server.runServerInMainThread()

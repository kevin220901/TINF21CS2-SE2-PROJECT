

import pickle
import socket
from networking.networkevent import NetworkEvent
from networking import constants



class SocketWrapper:
    '''
        deprecated (for now). 
        maby of use later
    '''

    def __init__(self, conn:socket.socket) -> None:
        self.__conn:socket.socket = conn


    def socket_sendall(self, data:bytes):
        self.__conn.sendall(data)


    def sendall(self, eventID:NetworkEvent, dataObj):
        body = pickle.dumps(dataObj)
        head = ((len(body) << 8) + eventID.value).to_bytes(constants.NETWORK_OBJECT_HEAD_SIZE_BYTES, 'big')

        self.__conn.sendall(head)
        self.__conn.sendall(body)
        pass

    def recv(self, __buffsize):
        return self.__conn.recv(__buffsize)


    def close(self):
        self.__conn.close
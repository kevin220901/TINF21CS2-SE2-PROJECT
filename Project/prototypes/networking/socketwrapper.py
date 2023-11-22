

import pickle
import socket
from Project.prototypes.networking.networkevent import NetworkEvent
import constants



class SocketWrapper:

    def __init__(self, conn:socket.socket) -> None:
        self.__conn = conn


    def socket_sendall(self, data:bytes):
        self.__conn.sendall(data)


    def sendall(self, eventID:NetworkEvent, dataObj):
        body = pickle.dumps(dataObj)
        head = ((len(body) << 8) + eventID.value).to_bytes(constants.NETWORK_OBJECT_HEAD_SIZE_BYTES, 'big')

        self.__conn.sendall(head)
        self.__conn.sendall(body)


    def rcv(self, __buffsize):
        return self.__conn.recv(__buffsize)


    def close(self):
        self.__conn.close

import pickle
import socket

import networking.constants as NetworkConst
from networking.networkevent import NetworkEvent


class NetworkClient:

    def __init__(self, host, port) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.id = self.__connect()


    def __connect(self):
        #TODO: Error handling
        self.client.connect(self.address)
        return self.client.recv(NetworkConst.CLIENT_ID_BYTELENGTH)
    

    def sync(self, eventId:NetworkEvent, data):
        eventData = pickle.dumps(data)
        eventHead = (len(eventData) << 8 + eventId.value).to_bytes(3, 'big')

        self.client.sendall(eventHead)
        self.client.sendall(eventData)


        recieved = self.client.recv(NetworkConst.MAX_EVENT_HEAD_SIZE_BYTES)
        recieved = int.from_bytes(recieved, 'big')

        eventId = recieved & NetworkConst.EVENT_HEAD_ID_MASK
        eventDataLength = (recieved & NetworkConst.EVENT_HEAD_DATA_LENGTH_MASK) >> 8

        recieved = self.client.recv(eventDataLength)
        eventData = pickle.loads(recieved)

        #TODO: the events need to be handled accordingly
        if eventId == NetworkEvent.MESSAGE.value:
            print(eventData)

        return eventData
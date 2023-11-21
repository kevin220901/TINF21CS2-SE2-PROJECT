
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
        self.client.sendall(eventId.value.to_bytes(1, 'big'))
        self.client.sendall(pickle.dumps(data))

        recieved = self.client.recv(NetworkConst.MAX_EVENT_ID_SIZE_BYTES)
        eventId = int.from_bytes(recieved, 'big')

        recieved = self.client.recv(NetworkConst.MAX_EVENT_DATA_SIZE_BYTES)
        eventData = pickle.loads(recieved)

        #TODO: the events need to be handled accordingly
        if eventId == NetworkEvent.MESSAGE.value:
            print(eventData)

        return eventData
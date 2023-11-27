
import pickle
import queue
import socket
import threading

import networking.constants as NetworkConst
from networking.networkevent import NetworkEvent



class NetworkObject:
    def __init__(self, head, boby) -> None:
        self.head:bytes = head
        self.body:bytes = boby


class NetworkEventObject:
    def __init__(self, eventId, eventData) -> None:
        self.eventId:NetworkEvent = eventId
        self.eventData:any = eventData

    def __str__(self) -> str:
        return f"'eventID':'{self.eventId}', 'eventData':'{self.eventData}'"



class NetworkClient:

    def __init__(self, host, port) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port)

        self.id = self.__connect()

        self.send_lock = threading.Lock()
        self.recieve_lock = threading.Lock()

        self.__sendQueue = queue.Queue(maxsize=10)
        self.__recvQueue = queue.Queue(maxsize=10)

        self.stopEvent = threading.Event()

        recieve_thread = threading.Thread(target=self.__recieve, daemon=True)
        send_thread = threading.Thread(target=self.__send, daemon=True)

        

        recieve_thread.start()
        send_thread.start()



    def __connect(self):
        #TODO: Error handling
        self.client.connect(self.address)
        return self.client.recv(NetworkConst.CLIENT_ID_BYTELENGTH)
    
    
    def read(self):
        '''
        returns the first element of the recieved queue
        '''
        if self.__recvQueue.empty(): return None
        return self.__recvQueue.get()
    

    def disconnect(self):
        pass
    
    
    def send(self, eventId:NetworkEvent, eventData):
        body = pickle.dumps(eventData)
        head = ((len(body) << 8) + eventId.value).to_bytes(3, 'big')
        
        self.__sendQueue.put(NetworkObject(head, body))


    def __send(self):
        while not self.stopEvent.is_set():
            if self.__sendQueue.empty():
                continue

            netObj:NetworkObject = self.__sendQueue.get()
            
            with self.send_lock:
                try:
                    self.client.sendall(netObj.head)
                    self.client.sendall(netObj.body)
                except Exception as e:
                    print(e)
                    break
                
                

    def __recieve(self):
        state = 0

        eventId = None
        eventData = None
        eventDataLength = None

        while not self.stopEvent.is_set():

            with self.recieve_lock:
                try:
                    if state == 0:
                        recieved = self.client.recv(NetworkConst.NETWORK_OBJECT_HEAD_SIZE_BYTES)
                        if not recieved:
                            continue

                        eventId = int.from_bytes(recieved[2:], 'big')
                        eventDataLength = int.from_bytes(recieved[:2], 'big')
                        state = 1

                    elif state == 1:
                        recieved = self.client.recv(eventDataLength)
                        if not recieved:
                            continue

                        eventData = pickle.loads(recieved)
                        self.__recvQueue.put(NetworkEventObject(eventId, eventData))
                        state = 0


                except Exception as e:
                    print(e)
                    self.client.close()
                    break

    
    def createLobby(self, lobbyName):
        eventId = NetworkEvent.LOBBY_CREATE
        eventData = {'lobbyName':lobbyName}
        self.send(eventId, eventData)
    
    def joinLobby(self, lobbyId):
        eventId = NetworkEvent.LOBBY_JOIN
        eventData = {'lobbyId':lobbyId}
        self.send(eventId, eventData)

    def leaveLobby(self):
        eventId = NetworkEvent.LOBBY_LEAVE
        eventData = {'':''}
        self.send(eventId, eventData)

    def ready(self):
        eventId = NetworkEvent.LOBBY_READY
        eventData = {'':''}
        self.send(eventId, eventData)

    def sendMessage(self, message):
        eventId = NetworkEvent.MESSAGE
        eventData = {'message':message}
        self.send(eventId, eventData)
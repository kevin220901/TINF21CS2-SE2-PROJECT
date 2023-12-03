
import json
import queue
import socket
import threading

import network.constants as NetworkConst
from network.networkevent import NetworkEvent

##################################################
## Author: Luis Eckert
##################################################

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



class ServerApi:

    def __init__(self, host, port) -> None:
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.__auth_token = None

        #move the actual connection to a public mthod to enable easier connect retries

        self.__connect()

        self.send_lock = threading.Lock()
        self.recieve_lock = threading.Lock()

        self.__sendQueue = queue.Queue(maxsize=10)
        self.__recvQueue = queue.Queue(maxsize=10)

        self.__stopEvent = threading.Event()

        self.__recieve_thread = threading.Thread(target=self.__recieve, daemon=True)
        self.__send_thread = threading.Thread(target=self.__send, daemon=True)

        self.__recieve_thread.start()
        self.__send_thread.start()

    def close(self):
        self.__stopEvent.set()
        self.__recvQueue
        #self.__send_thread.join()
        #self.__recieve_thread.join()
        pass

    def __connect(self):
        #TODO: Error handling
        self.__sock.connect(self.address)
        #return self.__sock.recv(NetworkConst.CLIENT_ID_BYTELENGTH)
    
    
    def recv(self):
        '''
        returns the first element of the recieved queue
        '''
        #if self.__recvQueue.empty(): return None
        return self.__recvQueue.get()
    

    def disconnect(self):
        self.__stopEvent.set()

        self.__send_thread.join()
        self.__recieve_thread.join()

        self.__sock.close()

    
    
    def send(self, eventId:NetworkEvent, eventData):
        body = bytes(json.dumps(eventData),'utf8')
        head = ((len(body) << 8) + eventId.value).to_bytes(3, 'big')
        
        self.__sendQueue.put(NetworkObject(head, body))


    def __send(self):
        while not self.__stopEvent.is_set():
            #if self.__sendQueue.empty():
            #    continue

            netObj:NetworkObject = self.__sendQueue.get()
            
            with self.send_lock:
                try:
                    self.__sock.sendall(netObj.head)
                    self.__sock.sendall(netObj.body)
                except Exception as e:
                    print(e)
                    break
                
                

    def __recieve(self):
        state = 0

        eventId = None
        eventData = None
        eventDataLength = None

        while not self.__stopEvent.is_set():

            with self.recieve_lock:
                try:
                    if state == 0:
                        recieved = self.__sock.recv(NetworkConst.NETWORK_OBJECT_HEAD_SIZE_BYTES)
                        if not recieved:
                            continue

                        eventId = int.from_bytes(recieved[2:], 'big')
                        eventDataLength = int.from_bytes(recieved[:2], 'big')
                        state = 1

                    elif state == 1:
                        recieved = self.__sock.recv(eventDataLength)
                        if not recieved:
                            continue

                        eventData = json.loads(recieved)
                        
                        if eventId == NetworkEvent.LOGIN_SUCCESS.value:
                            self.__auth_token = eventData['token']

                        self.__recvQueue.put(NetworkEventObject(eventId, eventData))
                        state = 0


                except Exception as e:
                    print(e)
                    self.__stopEvent.set()
                    #self.sock.close()
                    break

    
    def createLobby(self, lobbyName):
        eventId = NetworkEvent.LOBBY_CREATE
        eventData = {'token':self.__auth_token,'lobbyName':lobbyName}
        self.send(eventId, eventData)
    
    def joinLobby(self, lobbyId):
        eventId = NetworkEvent.LOBBY_JOIN
        eventData = {'token':self.__auth_token,'lobbyId':lobbyId}
        self.send(eventId, eventData)

    def leaveLobby(self):
        eventId = NetworkEvent.LOBBY_LEAVE
        eventData = {'token':self.__auth_token,}
        self.send(eventId, eventData)

    def ready(self):
        eventId = NetworkEvent.LOBBY_READY
        eventData = {'token':self.__auth_token,}
        self.send(eventId, eventData)

    def sendMessage(self, message):
        eventId = NetworkEvent.MESSAGE
        eventData = {'token':self.__auth_token,'message':message}
        self.send(eventId, eventData)

    def getLobbies(self):
        eventId = NetworkEvent.LOBBIES_GET
        eventData = {'token':self.__auth_token}
        self.send(eventId, eventData)

    def login(self, username, password):
        eventId = NetworkEvent.LOGIN
        eventData = {'username':username, 'password':password}
        self.send(eventId, eventData)
        pass

    def register(self, username, password, email):
        eventId = NetworkEvent.REGISTRATION
        eventData = {'username':username, 'password':password, 'email':email}
        self.send(eventId, eventData)
        pass

    def requestProfile(self):
        eventId = NetworkEvent.PROFILE_READ
        eventData = {'token':self.__auth_token}
        self.send(eventId, eventData)
        pass
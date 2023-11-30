

import pickle
import socket

from _thread import *
from sys import stderr
import threading
from networking.server.servereventhandler_lobbybrowse import ServerEventHandler_LobbyBrowse
from networking.server.serverhandler_gamestart import ServerEventHandler_GameStart
from networking.server.servereventhandler_lobbyleave import ServerEventHandler_LobbyLeave
from networking.server.servereventhandler_lobbyready import ServerEventHandler_LobbyReady
from networking.server.clientapi import ClientApi
from networking.server.serverhandler_chatmessage import ServerEventHandler_ChatMessage


from networking import *




class Server:
    def __init__(self, host:str, port:int, runAsDaemon:bool) -> None:
        self.__host = host
        self.__port = port
        self.__lobbies = {}
        self.__globalStopEvent = threading.Event()
        self.__server_handler_thread = threading.Thread(target=self.__threaded_server, 
                                              args=(self.__host, self.__port, self.__globalStopEvent),
                                              daemon=runAsDaemon)
        self.__client_threads = []

    def start(self):
        self.__server_handler_thread.start()

    def stop(self):
        self.__globalStopEvent.set()
        self.__server_handler_thread.join()

    
    def __threaded_client(self, sock:socket.socket, playerId, playerName, globalStopEvent:threading.Event, localStopEvent:threading.Event):
        
        #do i need to make this a critical section?
        #maby use contextvars? -> dont know jet how they are to be used
        sock.sendall(playerId)

       
        api = ClientApi(
            conn=sock,
            playerId=playerId,
            playerName=playerName,
            lobbies=self.__lobbies,
        )

        
        

        events = {
            NetworkEvent.LOBBY_JOIN.value: ServerEventHandler_LobbyJoin(),            
            NetworkEvent.LOBBY_CREATE.value: ServerEventHandler_LobbyCreate(),         
            NetworkEvent.LOBBY_LEAVE.value: ServerEventHandler_LobbyLeave(),                      
            NetworkEvent.LOBBY_READY.value: ServerEventHandler_LobbyReady(),                     
            NetworkEvent.LOBBIES_GET.value: ServerEventHandler_LobbyBrowse(),                      
            NetworkEvent.GAME_MOVE.value: ServerEventHandler(),                        
            NetworkEvent.GAME_START.value: ServerEventHandler_GameStart(),
            NetworkEvent.GAME_FINISH.value: ServerEventHandler(),                      
            NetworkEvent.MESSAGE.value: ServerEventHandler_ChatMessage()               
        }
        

        state = 0
        eventId = 0
        eventDataLength = 0

        while not globalStopEvent.is_set() and not localStopEvent.is_set():
            try:

                if state == 0:  
                    recieved = sock.recv(NetworkConst.NETWORK_OBJECT_HEAD_SIZE_BYTES)
                    if not recieved:
                        break
                    
                    eventId = int.from_bytes(recieved[2:], 'big')
                    eventDataLength = int.from_bytes(recieved[:2], 'big')

                    state = 1
                else:
                    recieved = sock.recv(eventDataLength)
                    if not recieved:
                        break

                    eventData = pickle.loads(recieved)
                    eventhandler:ServerEventHandler = events[eventId]
                    eventhandler.handleEvent(api, eventData)

                    state = 0
            except Exception as e:
                localStopEvent.set()
                stderr.write(f"'error':{e}")
                break
                
                
        api.leaveLobby()
        sock.close()
        print(f"{api.playerName} disconnected")


    def __threaded_server(self, host:str, port:int, globalStopEvent:threading.Event):
        playerCounter:int = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            s.bind((host, port))
            s.listen()
            print("Server started")
            print(f"Waiting for connections on {host}:{port}")

            while not globalStopEvent.is_set():
                sock, addr = s.accept()
                playerCounter += 1

                sock.setblocking(True)
                client_thread = threading.Thread(target=self.__threaded_client, 
                        args=(sock, 
                                playerCounter.to_bytes(16, 'big'), 
                                f'player_{playerCounter}', 
                                globalStopEvent, 
                                threading.Event()))
                client_thread.start()
                self.__client_threads.append(client_thread)
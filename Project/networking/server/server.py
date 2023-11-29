import logging
import pickle
import socket

from _thread import *
from sys import stderr
from networking.server.servereventhandler_lobbybrowse import ServerEventHandler_LobbyBrowse
from networking.server.serverhandler_gamestart import ServerEventHandler_GameStart
from networking.server.servereventhandler_lobbyleave import ServerEventHandler_LobbyLeave
from networking.server.servereventhandler_lobbyready import ServerEventHandler_LobbyReady
from networking.server.clientapi import ClientApi
from networking.server.serverhandler_chatmessage import ServerEventHandler_ChatMessage
from networking.common.socketwrapper import SocketWrapper

from networking import *

HOST = "localhost"
PORT = 5555


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    lobbies = {}
    connected = {}

    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        str(e)



    s.listen()
    print("Server started")
    print(f"Waiting for connections on {HOST}:{PORT}")

    

    def threaded_client(sock:socket.socket, playerId, playerName):
        
        #do i need to make this a critical section?
        #maby use contextvars? -> dont know jet how they are to be used
        sock.sendall(playerId)

       
        api = ClientApi(
            conn=sock,
            playerId=playerId,
            playerName=playerName,
            lobbies=lobbies,
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
        running = True

        while running:
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
                running = False
                stderr.write(f"'error':{e}")
                break
                
                
        api.leaveLobby()
        sock.close()
        print(f"{api.playerName} disconnected")
        


    playerCounter = 0
    
    while True:
        sock, addr = s.accept()
        playerCounter += 1

        sock.setblocking(True)

        start_new_thread(threaded_client, (sock, 
                                           playerCounter.to_bytes(16, 'big'), 
                                           f'player_{playerCounter}', ))
                                           






from server.logger import *
import json
import socket

from _thread import *
from sys import stderr
import threading
from server.servereventhandler import ServerEventHandler
from server.servereventhandler_login import ServerEventHandler_Login
from server.servereventhandler_lobbycreate import ServerEventHandler_LobbyCreate
from server.servereventhandler_lobbyjoin import ServerEventHandler_LobbyJoin 
from server.servereventhandler_lobbybrowse import ServerEventHandler_LobbyBrowse
from server.serverhandler_gamestart import ServerEventHandler_GameStart
from server.servereventhandler_lobbyleave import ServerEventHandler_LobbyLeave
from server.servereventhandler_lobbyready import ServerEventHandler_LobbyReady
from server.servereventhandler_register import ServerEventHandler_Register
from server.servereventhandler_profileread import ServerEventHandler_ProfileRead
from server.servereventhandler_profileupdate import ServerEventHandler_ProfileUpdate
from server.servereventhandler_profiledelete import ServerEventHandler_ProfileDelete
from server.servereventhandler_gameplacepiece import ServerEventHandler_GamePlacePiece
from server.servereventhandler_profileupdatepassword import ServerEventHandler_ProfileUpdatePassword
from server.servereventhandler_lobbyrefresh import ServerEventHandler_LobbyRefresh
from server.clientapi import ClientApi
from server.serverhandler_chatmessage import ServerEventHandler_ChatMessage
from common.networkevent import NetworkEvent
from common import constants as NetworkConst
import traceback    

##################################################
## Author: Luis Eckert
##################################################

class Server:
    def __init__(self, host:str, port:int, globalStopEvent:threading.Event) -> None:
        self.__host = host
        self.__port = port
        self.__lobbies = {}
        self.__globalStopEvent = globalStopEvent
        self.__server_handler_thread = threading.Thread(target=self.__threaded_server, 
                                              args=(self.__host, self.__port, self.__globalStopEvent),
                                              daemon=True)
        self.__client_threads = []
        self.__loggedInPlayers = set()

    def start(self):
        self.__server_handler_thread.start()

    
    def stop(self):
        self.__globalStopEvent.set()
        self.__server_handler_thread.join()

    
    def __threaded_client(self, sock:socket.socket, globalStopEvent:threading.Event, localStopEvent:threading.Event):
        #TODO:instead of returning the playerId a notification is returned indicating the process was successfull
        #sock.sendall(playerId)
       
        api = ClientApi(
            conn=sock,
            stopEvent=localStopEvent,
            lobbies=self.__lobbies,
            loggedInPlayers=self.__loggedInPlayers
        )

        api.connection.emit_SysMessage('connected')
        

        events = {
            NetworkEvent.LOBBY_JOIN.value: ServerEventHandler_LobbyJoin(api),            
            NetworkEvent.LOBBY_CREATE.value: ServerEventHandler_LobbyCreate(api),         
            NetworkEvent.LOBBY_LEAVE.value: ServerEventHandler_LobbyLeave(api),                      
            NetworkEvent.LOBBY_READY.value: ServerEventHandler_LobbyReady(api),                     
            NetworkEvent.LOBBIES_GET.value: ServerEventHandler_LobbyBrowse(api),                      
            NetworkEvent.GAME_PLACE_PIECE.value: ServerEventHandler_GamePlacePiece(api),                        
            NetworkEvent.GAME_START.value: ServerEventHandler_GameStart(api),
            NetworkEvent.GAME_FINISH.value: ServerEventHandler(api),                      
            NetworkEvent.MESSAGE.value: ServerEventHandler_ChatMessage(api),
            NetworkEvent.LOGIN.value: ServerEventHandler_Login(api),
            NetworkEvent.REGISTRATION.value: ServerEventHandler_Register(api),
            NetworkEvent.PROFILE_READ.value: ServerEventHandler_ProfileRead(api),
            NetworkEvent.PROFILE_DELETE.value: ServerEventHandler_ProfileDelete(api),
            NetworkEvent.PROFILE_UPDATE.value: ServerEventHandler_ProfileUpdate(api),
            NetworkEvent.PROFILE_UPDATE_PASSWORD.value: ServerEventHandler_ProfileUpdatePassword(api),
            NetworkEvent.LOBBY_REFRESH.value: ServerEventHandler_LobbyRefresh(api)          
        }
        

        state = 0
        eventId = 0
        eventDataLength = 0

        try:
            while not globalStopEvent.is_set() and not localStopEvent.is_set():
                try:

                    if state == 0:  
                        recieved = sock.recv(NetworkConst.NETWORK_OBJECT_HEAD_SIZE_BYTES)
                        if not recieved:
                            break
                        
                        eventId = int.from_bytes(recieved[2:], 'big')
                        eventDataLength = int.from_bytes(recieved[:2], 'big')

                        state = 1

                        #check if the client provided a valid eventId
                        if eventId not in events:
                            raise Exception(f'invalid eventId')  
                    else:
                        recieved = sock.recv(eventDataLength)
                        if not recieved:
                            break

                        #reject processing events from unauthenticated source and terminate the connection
                        #allow login and register events
                        if not api.hasAuthToken:
                            if eventId != NetworkEvent.LOGIN.value and eventId != NetworkEvent.REGISTRATION.value:
                                logger.info(f'access denied for {api.playerName}')
                                break

                        eventData = json.loads(recieved)
                        eventhandler:ServerEventHandler = events[eventId]
                        eventhandler.handleEvent(eventData)

                        state = 0
                except socket.error as e:
                    localStopEvent.set()

                    logger.critical(f'{str(e)} \n {traceback.format_exc()}')
                    #TODO:flush the recieve buffer to ensure the server does not hickup
                    break

        except Exception as e:
            logger.critical(f'{str(e)} \n {traceback.format_exc()}')
        finally:          
            #api.leaveLobby() #TODO: fix bug!!
            if api.currentLobby:
                api.currentLobby.leave(api)

            if api.playerId in self.__loggedInPlayers:
                self.__loggedInPlayers.remove(api.playerId)
                
            sock.close()
            logger.info(f'{api.playerName} disconnected')
            #print(f"{api.playerName} disconnected")


    def __threaded_server(self, host:str, port:int, globalStopEvent:threading.Event):
        logger.info(f'... starting blokus server on {host}:{port}')

        playerCounter:int = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            logger.info(f"... server listening on {host}:{port}")

            while not globalStopEvent.is_set():
                
                sock, addr = s.accept()

                logger.info(f'>>> incomming connection from: {str(addr)}')
                #logger.info(f'>>> starting new client thread')
                sock.setblocking(True)
                client_thread = threading.Thread(target=self.__threaded_client, 
                        args=(sock, 
                                globalStopEvent, 
                                threading.Event()),
                                daemon=True
                            )
                
                client_thread.start()
                logger.info(f'... client thread {client_thread.ident} started')
                self.__client_threads.append(client_thread)
        return
    
    def runServerInMainThread(self):
        self.__threaded_server(self.__host, self.__port, self.__globalStopEvent)
        return
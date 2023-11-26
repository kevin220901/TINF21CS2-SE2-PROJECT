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
from networking.socketwrapper import SocketWrapper

from networking import *

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"





HOST = "localhost"
PORT = 5555


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    lobbies = {}
    connected = {}

    logging.info('>>Initializing ServerEventHandlers')

    logging.info('<<ServerEventHandlers Initialized')
    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        str(e)



    s.listen()
    print("Server started")
    print(f"Waiting for connections on {HOST}:{PORT}")

    

    def threaded_client(context):
        
        #do i need to make this a critical section?
        #maby use contextvars? -> dont know jet how they are to be used
        sock:socket.socket = context['conn']
        sock.sendall(context['playerId'])

        playerName = context['playerName'],
        
        logging.basicConfig(filename=f'dev_server_conn{playerName}.log', encoding='utf-8', 
            level=logging.DEBUG,
            format= LOG_FORMAT,datefmt='%d/%m/%Y %H:%M:%S')

        
        api = ClientApi(
            conn=sock,
            playerId=context['playerId'],
            playerName=playerName,
            lobbies=lobbies,
            logger = logging.getLogger()
        )

        
        

        events = {
            NetworkEvent.LOBBY_JOIN.value: ServerEventHandler_LobbyJoin(),             #data: playerId, lobbyId
            NetworkEvent.LOBBY_CREATE.value: ServerEventHandler_LobbyCreate(),         #data: tbd ...
            NetworkEvent.LOBBY_LEAVE.value: ServerEventHandler_LobbyLeave(),                      #data: playerId
            NetworkEvent.LOBBY_READY.value: ServerEventHandler_LobbyReady(),                      #data: playerId
            NetworkEvent.LOBBYS_GET.value: ServerEventHandler_LobbyBrowse(),                       #data: playerId
            NetworkEvent.GAME_MOVE.value: ServerEventHandler(),                        #data: playerId, pieceId
            NetworkEvent.GAME_START.value: ServerEventHandler_GameStart(),
            NetworkEvent.GAME_FINISH.value: ServerEventHandler(),                      #data: LobbyId, winner
            NetworkEvent.MESSAGE.value: ServerEventHandler_ChatMessage()               #data: playerId, message 
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
                        continue
                    
                    eventId = int.from_bytes(recieved[2:], 'big')
                    eventDataLength = int.from_bytes(recieved[:2], 'big')

                    state = 1
                else:
                    recieved = sock.recv(eventDataLength)
                    if not recieved:
                        continue

                    eventData = pickle.loads(recieved)
                    eventhandler:ServerEventHandler = events[eventId]
                    eventhandler.handleEvent(api, eventData)

                    state = 0
            except Exception as e:
                running = False
                api.logger.critical(e)

                api.leaveLobby()
                conn.close()
                stderr.write(f"'error':{e}")
                
        
        print(f"Disconnected from {addr}")
        


    playerCounter = 0
    
    while True:
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        playerCounter += 1

        context = {
            'conn':conn, 
            'addr':addr,
            'playerId':playerCounter.to_bytes(16, 'big'),
            'playerName':f'player_{playerCounter}'
        }

        start_new_thread(threaded_client, (context,))



import pickle
import socket
from _thread import *

from networking import *



HOST = "localhost"
PORT = 5555


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    lobbies = {}

    events = {
        NetworkEvent.LOBBY_JOIN.value: ServerEventHandler_LobbyJoin(),             #data: playerId, lobbyId
        NetworkEvent.LOBBY_CREATE.value: ServerEventHandler_LobbyCreate(),         #data: tbd ...
        NetworkEvent.LOBBY_LEAVE.value: ServerEventHandler(),                      #data: playerId
        NetworkEvent.LOBBY_READY.value: ServerEventHandler(),                      #data: playerId
        NetworkEvent.LOBBYS_GET.value: ServerEventHandler(),                       #data: playerId
        NetworkEvent.GAME_MOVE.value: ServerEventHandler(),                        #data: playerId, pieceId
        NetworkEvent.GAME_FINISH.value: ServerEventHandler(),                      #data: LobbyId, winner
        NetworkEvent.MESSAGE.value: ServerEventHandler()                           #data: playerId, message 
    }


    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        str(e)



    s.listen()
    print("Server started")
    print(f"Waiting for connections on {HOST}:{PORT}")

    

    def threaded_client(context):
        conn = context['conn']

        conn.send(context['playerId'])

        state = 0

        while True:
            try:

                if state == 0:  
                    recieved = conn.recv(NetworkConst.MAX_EVENT_ID_SIZE_BYTES)
                    if not recieved:
                        continue
                    eventId = int.from_bytes(recieved, 'big')
                    state = 1
                else:
                    recieved = conn.recv(NetworkConst.MAX_EVENT_DATA_SIZE_BYTES)
                    if not recieved:
                        continue
                    eventData = pickle.loads(recieved)
                    eventhandler = events[eventId]
                    eventhandler.handleEvent(context, eventData)
                    state = 0
            except:
                break
            
        conn.close()
        print(f"Disconnected from {addr}")


    playerCounter = 0

    while True:
        conn, addr = s.accept()
        print(f"Connected to {addr}")
        
        playerCounter += 1

        context = {
            'conn':conn, 
            'addr':addr,
            'lobbies':lobbies, 
            'playerId':playerCounter.to_bytes(16, 'big')
        }

        start_new_thread(threaded_client, (context,))


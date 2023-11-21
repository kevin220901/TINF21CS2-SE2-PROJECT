


import pickle
import socket

from networking.networkevent import NetworkEvent


class ServerEventHandler:

    def handleEvent(self, conn:socket.socket, eventData):
        print("handle event")
        conn.sendall(NetworkEvent.MESSAGE.value.to_bytes(1, 'big'))
        conn.sendall(pickle.dumps({'from':'server', 'message':'this event is being handled by the eventhandler'}))
        

class ServerEventHandler_JoinLobby(ServerEventHandler):
    
    def handleEvent(self, conn: socket, eventData):
        #Do stuff to handle player joining lobby
        pass
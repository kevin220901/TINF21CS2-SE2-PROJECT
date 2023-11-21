


import pickle
import socket

from networking.networkevent import NetworkEvent


class ServerEventHandler:

    def handleEvent(self, context, eventData):
        print("handle event")
        conn: socket.socket = context['conn']
        conn.sendall(NetworkEvent.MESSAGE.value.to_bytes(1, 'big'))
        conn.sendall(pickle.dumps({'from':'server', 'message':'this event is being handled by the eventhandler'}))
        


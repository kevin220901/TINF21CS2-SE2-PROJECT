


import pickle
import socket

from networking.networkevent import NetworkEvent


class ServerEventHandler:

    def handleEvent(self, context, eventData):
        print("handle event")
        conn: socket.socket = context['conn']


        body = pickle.dumps({'from':'server', 'message':'this event is being handled by the eventhandler'})
        head = ((len(body) << 8) + NetworkEvent.MESSAGE.value).to_bytes(3, 'big')

        conn.sendall(head)
        conn.sendall(body)
        


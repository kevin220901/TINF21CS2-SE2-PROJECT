
from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler

##################################################
## Author: Luis Eckert
##################################################

class ServerEventHandler_Login(ServerEventHandler):
    
    def handleEvent(self, client:ClientApi, eventData):
        if 'username' not in eventData or 'password' not in eventData:
            client.sendSysMessage('invalid eventData: missing credentials')
            
        client.login(eventData['username'], eventData['password'])

        pass
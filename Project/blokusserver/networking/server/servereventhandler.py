


from server.clientapi import ClientApi

class ServerEventHandler:

    def handleEvent(self, client:ClientApi, eventData):

        client.sendSysMessage('this event is being handled by the eventhandler')
        pass
    

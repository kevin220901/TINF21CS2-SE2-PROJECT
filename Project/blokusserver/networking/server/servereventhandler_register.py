


from server.clientapi import ClientApi
from server.servereventhandler import ServerEventHandler


class ServerEventHandler_Register(ServerEventHandler):
    def __init__(self, client:ClientApi):
        super().__init__(client)
    
    def handle(self, data):
        ## TODO:Check if username is already taken
        ## TODO:Check if username is valid
        ## TODO:Check if password is valid
        ## Register user
        self._client.register(data["username"], data["password"], data['email'])
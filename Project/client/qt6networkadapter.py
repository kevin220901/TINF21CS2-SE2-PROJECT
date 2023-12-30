
import threading
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from network.serverapi import NetworkEventObject, ServerApi, NetworkEvent
from network import constants as NetworkConst




class PyQt6_Networkadapter:
    def __init__(self, main_window, host, port) -> None:
        self.__main_window: BlokusUtility = main_window
        self.__api = ServerApi(host, port)

        self.__init_network_thread()
        pass

    def __init_network_thread(self):
        self.network_thread = QNetworkThread(self.__api, self.__main_window)
        self.network_thread.start()
        pass

    def stop(self):
        self.network_thread.stop()
        pass
    
    def addNetworkEventHandler(self, event:NetworkEvent, handler):
        self.network_thread.event_map[event.value].connect(handler)
        pass
    
    def removeNetworkEventHandler(self, event:NetworkEvent, handler):
        self.network_thread.event_map[event.value].disconnect(handler)
        pass

    @property
    def api(self) -> ServerApi:
        return self.__api


    pass
    
class QNetworkEventSignals(QObject):
    recv_sys_message = pyqtSignal(NetworkEventObject)
    recv_messsage = pyqtSignal(NetworkEventObject)
    login_success = pyqtSignal(NetworkEventObject)
    lobby_created = pyqtSignal(NetworkEventObject)
    lobby_joined = pyqtSignal(NetworkEventObject)
    lobby_update = pyqtSignal(NetworkEventObject)
    lobby_browser = pyqtSignal(NetworkEventObject)
    game_start = pyqtSignal(NetworkEventObject)
    game_update = pyqtSignal(NetworkEventObject)
    game_invalid_placement = pyqtSignal(NetworkEventObject)
    game_end = pyqtSignal(NetworkEventObject)
    registration_success = pyqtSignal(NetworkEventObject)
    profile_read = pyqtSignal(NetworkEventObject)
    profile_delete = pyqtSignal(NetworkEventObject)
    profile_update = pyqtSignal(NetworkEventObject)
    pass
    
    

class QNetworkThread(QThread):
    def __init__(self, api:ServerApi, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.__api = api
        self.eventSignals = QNetworkEventSignals()
        self.__stopEvent = threading.Event()
        self.event_map = {
            NetworkEvent.SYSMESSAGE.value: self.eventSignals.recv_sys_message,
            NetworkEvent.MESSAGE.value: self.eventSignals.recv_messsage,
            NetworkEvent.LOGIN_SUCCESS.value: self.eventSignals.login_success,
            NetworkEvent.LOBBY_JOIN.value: self.eventSignals.lobby_joined,
            NetworkEvent.LOBBY_CREATE.value: self.eventSignals.lobby_created,
            NetworkEvent.LOBBIES_GET.value: self.eventSignals.lobby_browser,
            NetworkEvent.LOBBY_UPDATE.value: self.eventSignals.lobby_update,
            #NetworkEvent.LOBBY_JOIN.value: self.eventSignals.lobby_new_host,
            NetworkEvent.GAME_START.value: self.eventSignals.game_start,
            NetworkEvent.GAME_UPDATE.value: self.eventSignals.game_update,
            NetworkEvent.GAME_INVALID_PLACEMENT.value: self.eventSignals.game_invalid_placement,
            NetworkEvent.REGISTRATION_SUCCESS.value: self.eventSignals.registration_success,
            NetworkEvent.PROFILE_READ.value: self.eventSignals.profile_read,
            NetworkEvent.PROFILE_DELETE.value: self.eventSignals.profile_delete,
            NetworkEvent.PROFILE_UPDATE.value: self.eventSignals.profile_update
        }
    
    def run(self):
        while not self.__stopEvent.is_set():
            event:NetworkEventObject = self.__api.recv()
            self.event_map[event.eventId].emit(event)
            
        return

    def stop(self):
        self.__stopEvent.set()
        self.__api.close()
        return
    






from main import BlokusUtility

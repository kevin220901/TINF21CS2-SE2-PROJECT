
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


    @property
    def api(self):
        return self.__api


    pass
    
class QNetworkEventSignals(QObject):
    sys_message = pyqtSignal(NetworkEventObject)
    messsage = pyqtSignal(NetworkEventObject)
    login = pyqtSignal(NetworkEventObject)
    lobby_create = pyqtSignal(NetworkEventObject)
    pass
    
    

class QNetworkThread(QThread):
    def __init__(self, api:ServerApi, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.__api = api
        self.eventSignals = QNetworkEventSignals()
        self.__stopEvent = threading.Event()
        self.event_map = {
            NetworkEvent.SYSMESSAGE.value: self.eventSignals.sys_message,
            NetworkEvent.MESSAGE.value: self.eventSignals.messsage,
            NetworkEvent.LOGIN.value: self.eventSignals.login,
            NetworkEvent.LOBBY_CREATE.value: self.eventSignals.lobby_create
        }
    
    def run(self):
        while not self.__stopEvent.is_set():
            event:NetworkEventObject = self.__api.recv()
            self.event_map[event.eventId].emit(event)
            
        pass

    def stop(self):
        self.__stopEvent.set()
        self.__api.close()
        pass
    pass






from main import BlokusUtility

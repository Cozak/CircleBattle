from CoNetworkServerM import *
from CoNetworkClientM import *
from CoNetworkHTTPM import *

# help with multi-player's communication with UDP
class CoNetworkCenter:
    def __init__(self):
        self.net_server = CoNetworkServer()
        self.net_client = CoNetworkClient()
        self.net_web = CoNetworkHTTP()
    # Server
    def buildNewServer(self, addr, backlog=NET_DEFAULT_BACKLOG, timeout=NET_DEFAULT_TIMEOUT):
        self.net_server.closeServer()
        return self.net_server.buildServer(addr, backlog, timeout)
    def closeServer(self):
        if not self.net_server.isClose():
            self.net_server.closeServer()
    def setRegisterUpdateForServer(self, target):
        self.net_server.registerUpdate(target)
    def getServerRunTask(self):
        return self.net_server.run
    def sendDataToAllClient(self, data):
        self.net_server.sendToAllClient(data)
    def sendDataToClient(self, player_id, data):
        self.net_server.sendToClient(player_id, data)
    def notifyAllClientWithPlayerID(self):
        try:
            player_ids = self.net_server.getValidPlayerIDList()[1:]
            # print(player_ids)
            map(self.net_server.sendToClient, player_ids, [self.packData((-1, player_id)) for player_id in player_ids])
        except Exception, e:
            print("Notify Failed ", e)
    def getValidClientPlayerIDS(self):
        return self.net_server.getValidPlayerIDList()
    # Client
    def buildNewClient(self, addr, timeout=NET_DEFAULT_TIMEOUT):
        self.net_client.closeClient()
        return self.net_client.buildClient(addr, timeout)
    def closeClient(self):
        if not self.net_client.isClose():
            self.net_client.closeClient()
    def setRegisterUpdateForClient(self, target):
        self.net_client.registerUpdate(target)
    def getClientRunTask(self):
        return self.net_client.run
    def sendDataToServer(self, data):
        self.net_client.sendToServer(data)
    # HTTP
    def setHTTPHost(self, addr): # set http host
        self.net_web.setTargetHost(addr)
    # use http protocol to post game record
    def postHTTPData(self, para_dict): 
        self.net_web.postData(para_dict)
    # Tools
    # pack and unpack data
    def packData(self, obj_data):
        return pickle.dumps(obj_data)
    def unpackData(self, str_data):
        return pickle.loads(str_data)
    def quit(self):
        self.closeClient()
        self.closeServer()
        pass

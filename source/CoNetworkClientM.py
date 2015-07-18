from CoSource import *

# In Multi-Player Mode As Client
class CoNetworkClient:
    def __init__(self):
        self.local_client = None
        self.dest_addr = ()
        self.timeout = 0
        self.is_alive = False
        self.buffer_size = BUFFER_SIZE
        self.notify_update = lambda data : None
    def buildClient(self, addr, timeout=0):
        self.local_client = socket.socket()
        self.dest_addr = addr
        self.timeout = timeout
        print("Building Game Client")
    def isClose(self):
        return not self.is_alive
    def closeClient(self):
        self.is_alive = False
        try:
            if self.local_client:
                self.local_client.close()
        except Exception, e:
            print("Client Close Failed ", e)
    def run(self): # receiver
        try:
            self.local_client.connect(self.dest_addr)
            self.is_alive = 1
            print("Game Client Listening")
            while self.is_alive:
                try:
                    data = self.local_client.recv(self.buffer_size)
                    self.notify_update(data)
                except Exception, e:
                    print('Game-Client Disconnect ', e)
                    self.is_alive = False
        except Exception, e:
            print('Failed to connect Game-Server: ', self.dest_addr, ' With Error ', e)
        finally:
            # close and reset
            self.local_client.close()
            self.local_client = None
            print('Game-Client Closed')
    def sendToServer(self, data):
        if data and self.is_alive:
            try:
                self.local_client.send(data)
                return True
            except Exception, e:
                print("SendToServer Failed ", e)
        return False
    def registerUpdate(self, target):
        if target:
            self.notify_update = target



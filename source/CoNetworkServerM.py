from CoSource import *

# In Multi-Player Mode As Server
# Game-Server distribute each Frame and Menu-feedback to Game-Client
# Game-Server also subimits real-time statement of every player to Web-Server
class CoNetworkServer:
    def __init__(self):
        self.local_server = None
        self.cur_addr = ()
        self.player_socket_map = {}
        self.socket_player_map = {}
        self.backlog = 0
        self.timeout = 0
        self.islock = False
        self.buffer_size = BUFFER_SIZE
        self.is_alive = False
        self.player_id_list = COPLAYERLIST[:] # copy list
        self.notify_update = lambda pid, data : None
    def buildServer(self, addr, backlog, timeout): # addr = (host, port); backlog > 0, timeout >= 0
        # init
        self.local_server = None
        self.cur_addr = ()
        self.player_socket_map = {}
        self.socket_player_map = {}
        self.backlog = 0
        self.timeout = 0
        self.islock = False
        try:
            self.timeout = timeout
            self.cur_addr = addr
            self.backlog = backlog
            self.local_server = socket.socket()
            self.local_server.bind(self.cur_addr)
        except Exception, e:
            if self.local_server:
                self.local_server.close()
                self.local_server = None
            print('Game-Server build failed ', e)
            return False
        print("Building Game Server")
        return True
    def isClose(self):
        return not self.is_alive
    def closeServer(self):
        self.is_alive = False
        try:
            if self.local_server:
                self.local_server.close()
        except Exception, e:
            print("Server Close Failed ", e)
    def unlockPlayers(self):
        self.islock = False
    def lockPlayers(self):
        self.islock = True
    def getValidPlayerIDList(self):
        return self.player_socket_map.keys()
    def run(self): # run as a receiver
        self.local_server.listen(self.backlog)
        self.player_socket_map[self.player_id_list[0]] = self.local_server # host is always player_0
        self.socket_player_map[self.local_server.fileno()] = self.player_id_list[0]
        self.is_alive = True
        print("Game Server Listening")
        while self.is_alive:
            rl, wl, el = select.select(self.player_socket_map.values(), [], [], self.timeout)
            for r in rl:
                if r is self.local_server: # get new client
                    if not self.islock and len(self.socket_player_map) < len(self.player_id_list): # game-client can't join this game when started
                        try:
                            cl, addr = r.accept()
                            new_id = self.player_id_list[len(self.player_socket_map)]
                            print("New Client Id: ", new_id)
                            self.player_socket_map[new_id] = cl
                            self.socket_player_map[cl.fileno()] = self.player_id_list[len(self.socket_player_map)]
                            print('New Game-Client Connect: ', addr)
                        except Exception, e:
                            print("Accept Failed ", e)
                else:
                    player_id = self.socket_player_map[r.fileno()]
                    try:
                        data = r.recv(self.buffer_size)
                        self.notify_update(player_id, data)
                    except Exception, e:
                        print('Game-Client Disconnect: ', r.getpeername(), 'With Error ', e)
                        del self.socket_player_map[r.fileno()]
                        del self.player_socket_map[player_id]
                        self.player_id_list.remove(player_id)
                        self.player_id_list.append(player_id) # move this player_id to the tail
                        r.close()
        # ready to quit
        for sk in self.player_socket_map.values()[1:]:
            sk.close()
        self.local_server = None
        print('Game-Server Quit')
    def sendToAllClient(self, data):
        if data:
            for player_id in self.player_socket_map.keys()[1:]:
                self.sendToClient(player_id, data)
    def sendToClient(self, player_id, data): # all data sent via this method
        if data and self.is_alive and player_id in self.player_socket_map:
            try:
                self.player_socket_map[player_id].send(data)
                return True
            except Exception, e:
                print("SendToClient Error", e)
        return False
    def registerUpdate(self, target):
        if target:
            self.notify_update = target

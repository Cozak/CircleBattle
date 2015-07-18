from __future__ import print_function
from CoSource import *

# Socket Model
from CoNetwork import *
# Render Work here, for local player only
from CoRenderM import *
# Input Device Controller
from CoControllerM import *
# Physics World Model
from CoPhyWorldM import *

# Hold all models
class CoGame:
    def __init__(self):
        # self.initGameSystem()
        self.game_clock = pygame.time.Clock()
        self.render_clock = pygame.time.Clock()
        self.net_clock = pygame.time.Clock()
        self.pyrender = CoRender(SCREEN)
        self.phyworld = CoPhyWorld()
        self.controller = CoController()
        self.net_handler = CoNetworkCenter()
        self.data_collector = None
        # public Storage
        self.game_mode = GAME_MODE_DEFAULT # GAME_MODE_DEFAULT, GAME_MODE_SINGLE, GAME_MODE_MULTI_CLIENT, GAME_MODE_MULTI_SERVER
        self.render_queue = [[], [], [], []]
        # self.render_center = [[0, 0],
        #                       [0, 0],
        #                       [0, 0],
        #                       [0, 0]]
        self.game_player_id = COPLAY_0
        self.net_addr = SERVER_ADDR
    # def initGameSystem(self):
    #     pygame.init()
    def setLocalPlayerID(self, player_id):
        self.game_player_id = player_id
        # if self.controller:
        #     self.controller.setLocalPlayerID(player_id)
    def setCurrentGameMode(self, game_mode):
        self.game_mode = game_mode
    def setHTTPHost(self, addr):
        self.net_handler.setHTTPHost(addr)
    def setNetworkAddr(self, addr):
        if addr:
            self.net_addr = addr
    def clearAndQuitGamePass(self):
        self.phyworld.clearPhyWorld()
        self.controller.clearControllor()
        self.clearRenderQueue()
    def quit(self):
        # update: call tel-player to quit
        self.net_handler.quit()
        self.phyworld.quit()
        self.pyrender.quit()
        self.controller.quit()
        # pygame.quit()
    def updateGameSystem(self):    # update the statement of sys
        # keys = self.controller.getKeyPress(self.game_player_id)
        keys = self.controller.getKeyPress(COPLAY_0)
        return keys and keys[K_ESCAPE]
    def deployGamePass(self, gpass):    # for test only
        gpass.deploy(self.phyworld)
    def setDataCollector(self, data_collector):
        if data_collector:
            self.data_collector = data_collector
    def setCollidListener(self, new_listener):
        if new_listener:
            self.phyworld.b2dworld.contactListener = new_listener
    def setCollidFilter(self, new_filter):
        if new_filter:
            self.phyworld.b2dworld.contactFilter = new_filter
    def setRayCastCallback(self, new_raycast_callback):
        if new_raycast_callback:
            self.phyworld.raycast_callback = new_raycast_callback
    # for render task
    def pushRenderQueue(self, render_info):
        if render_info:
            for (player_id, player_render_list) in zip(COPLAYERLIST, render_info):
                self.render_queue[player_id].insert(0, tuple(player_render_list))
                while len(self.render_queue[player_id]) > 3:
                    self.render_queue[player_id].pop()
    def clearRenderQueue(self):
        for plist in self.render_queue:
            while len(plist) > 0:
                plist.pop()
        # for pid in COPLAYERLIST:
        #     self.render_center[pid] = [0, 0]
    # def updateRenderCenter(self, render_center):
    #     if render_center:
    #         for (player_id, view_render_center) in zip(COPLAYERLIST, render_center):
    #             self.render_center[player_id] = view_render_center
    def NetworkLoop(self):   # socket, render, controller
        while 1: # init
            try:
                cur_game_mode = self.game_mode
                # print("Current Game Mode: ", cur_game_mode)
                if cur_game_mode == GAME_MODE_DEFAULT:
                    while cur_game_mode == self.game_mode: # if mode change break
                        self.net_clock.tick(HTTP_FPS)
                        pass
                elif cur_game_mode == GAME_MODE_SINGLE:
                    while cur_game_mode == self.game_mode: # if mode change break
                        self.net_clock.tick(HTTP_FPS)
                        if self.data_collector and self.data_collector.isReady():
                            # get and post upload data
                            self.net_handler.postHTTPData(self.data_collector.getUploadData())
                elif cur_game_mode == GAME_MODE_MULTI_CLIENT:
                    # registe callback function
                    def updateRenderInfoForClient(str_data):
                        try:
                            obj_data = self.net_handler.unpackData(str_data)
                            # print("My Client Get Data")
                            if obj_data:
                                if isinstance(obj_data[0], int): # notify
                                    # print("My Client ID: ", obj_data[1])
                                    self.setLocalPlayerID(obj_data[1])
                                else:
                                    # self.updateRenderCenter((obj_data[0],))
                                    self.pyrender.updateRenderOrigin(obj_data[0])
                                    self.pushRenderQueue((obj_data[1],))
                        except Exception, e:
                            print("Client Listener Failed ", e)
                    self.net_handler.buildNewClient(self.net_addr)
                    self.net_handler.setRegisterUpdateForClient(updateRenderInfoForClient)
                    listener_thread = threading.Thread(target=self.net_handler.getClientRunTask())
                    listener_thread.setDaemon(True)
                    listener_thread.start()
                    while cur_game_mode == self.game_mode and listener_thread.isAlive(): # if mode change break
                        str_data = self.net_handler.packData((self.controller.getMousePos(COPLAY_0),
                                                            self.controller.getMousePress(COPLAY_0),
                                                            self.controller.getKeyPress(COPLAY_0)))
                        self.net_handler.sendDataToServer(str_data)
                        self.net_clock.tick(TARGET_FPS)
                    else:
                        print("In Network Loop Close Client")
                        self.net_handler.closeClient()
                elif cur_game_mode == GAME_MODE_MULTI_SERVER:
                    # registe callback function
                    def updateRenderInfoForServer(player_id, str_data):
                        # update valid player_ids
                        obj_data = self.net_handler.unpackData(str_data)
                        # print(obj_data[0], obj_data[1])
                        if obj_data:
                            # if obj_data[0] < COPLAYER_MEUN_DIFF: # update controller info
                            self.controller.updateControllerFromNetwork((player_id, obj_data))
                            # else: # update menu choice
                            #     self.controller.updateMenuCommand((player_id, obj_data))
                    self.net_handler.buildNewServer(self.net_addr)
                    self.net_handler.setRegisterUpdateForServer(updateRenderInfoForServer)
                    listener_thread = threading.Thread(target=self.net_handler.getServerRunTask())
                    listener_thread.setDaemon(True)
                    listener_thread.start()
                    notify_time = NET_SERVER_NOTIFY_DIFF
                    while cur_game_mode == self.game_mode and listener_thread.isAlive(): # if mode change break
                        self.net_clock.tick(SERVER_FPS)
                        if notify_time >= NET_SERVER_NOTIFY_DIFF: # notify all client
                            self.net_handler.notifyAllClientWithPlayerID(); notify_time = 0
                        # str_data = self.net_handler.packData((self.render_center, self.render_queue[0]))
                        viewpos_list = self.phyworld.getViewPoint()
                        valid_player_list = self.net_handler.getValidClientPlayerIDS()[1:]
                        for player_id in COPLAYERLIST[1:]: # send data to each client separated by player_id
                            if player_id in valid_player_list: # if valid
                                str_data = self.net_handler.packData((viewpos_list[player_id],
                                                                      self.render_queue[player_id][0]))
                                self.net_handler.sendDataToClient(player_id, str_data)
                                # self.net_handler.sendDataToAllClient(str_data)
                        notify_time += 1
                    else:
                        print("In Network Loop Close Server")
                        self.net_handler.closeServer()
            except Exception, e:
                print("Network Loop Error ", e)
    def RenderLoop(self):
        while 1: # Over while Main Loop Quit
            try:
                # if self.render_queue and self.render_center:
                if self.render_queue[COPLAY_0]:
                    # self.pyrender.updateRenderOrigin(self.render_center[self.game_player_id],
                    # self.controller.getMousePos(self.game_player_id))    # update the center of screen
                    # self.pyrender.updateRenderOrigin(self.phyworld.getViewPoint()[COPLAY_0])
                    self.pyrender.renderProcessor(self.render_queue[COPLAY_0][0]) # just for local render
                    self.pyrender.renderDisplay()
                    self.render_clock.tick(TARGET_FPS)
            except Exception, e:
                print("Render Loop Error ", e)
    def GameLoop(self):
        while 1:
            try:
                # print("Sys: In Loop")
                self.controller.updateLocalController()
                if self.updateGameSystem():
                    break
                self.phyworld.worldStep()
                self.phyworld.worldStep()
                self.phyworld.clearGroupRenderInfo() # clear old info
                self.phyworld.updateAllEntity()
                render_info = self.phyworld.exportGroupsRenderInfo()
                # render_center = self.phyworld.getViewPoint()
                # update: call self.socketHanlder.submitAndSend
                self.pushRenderQueue(render_info)
                self.pyrender.updateRenderOrigin(self.phyworld.getViewPoint()[COPLAY_0])
                # self.updateRenderCenter(render_center)
                # self.pyrender.updateRenderOrigin(render_center[COPLAY_0], self.controller.getMousePos())
                # self.pyrender.renderProcessor(render_info)
                # self.pyrender.renderDisplay()
                self.game_clock.tick(TARGET_FPS)
            except Exception, e:
                print("Game Loop Error ", e)
        # self.quit()
    def ClientGameLoop(self):
        while 1:
            # print("Sys: In Loop")
            self.controller.updateLocalController()
            if self.updateGameSystem():
                break 
    def setTestGamePass(self, gpass):
        self.test_gamepass = gpass
    def initGameSys(self):
        # init
        self.phyworld.setPhyController(self.controller)
        # launch Render Thread
        t_render = threading.Thread(target=self.RenderLoop)
        t_render.setDaemon(True)
        t_render.start()
        t_network = threading.Thread(target=self.NetworkLoop)
        t_network.setDaemon(True)
        t_network.start()
        # define renderFilterGenenrator
        def renderFilterGenerator():
            valid_player_ids =  (COPLAY_0,) if self.game_mode == GAME_MODE_SINGLE else self.net_handler.getValidClientPlayerIDS()
            all_player_mouse_pos = [self.controller.getMousePos(pid) for pid in COPLAYERLIST]
            all_player_dynamic_viewpoint = self.phyworld.getViewPoint()
            def renderFilter(entity_pos):
                for vplayer_id in valid_player_ids:
                    if self.pyrender.isInSight(entity_pos, all_player_dynamic_viewpoint[vplayer_id]):
                        yield vplayer_id
            return renderFilter
        self.phyworld.registeFilterGenerator(renderFilterGenerator)
    def ALLStart(self): # launch the game system with multi-thread
        self.initGameSys()
        # sample loop
        while 1:
            try:
                self.clearAndQuitGamePass()
                self.setCurrentGameMode(GAME_MODE_DEFAULT)
                print('\nGame Menu\n\n1. Single-Player\n\n2. Multi-Player\n\n3. Options\n\nX. Quit\n')
                res = raw_input('>>')
                if not res.isdigit():
                    continue
                elif int(res) == 1: # Single-Player Mode
                    self.setLocalPlayerID(COPLAY_0)
                    self.setCurrentGameMode(GAME_MODE_SINGLE)
                    self.deployGamePass(self.test_gamepass) # deploy game pass
                    self.GameLoop()
                elif int(res) == 2: # Multi-Player Mode
                    ress = raw_input('\n1. Build Up A New Game\n\n2. Join Others\n\n3. Back\n\n>>')
                    if ress.isdigit():
                        if int(ress) == 1:
                            ip_port = raw_input("\nInput Local Host Port >>") # rs is a tuple
                            print("...setting network...")
                            # self.setNetworkAddr((ip_port[0], int(ip_port[1])))
                            self.setNetworkAddr((socket.gethostbyname(socket.gethostname()), int(ip_port)))
                            print("...network ready...")
                            self.setLocalPlayerID(COPLAY_0)
                            self.setCurrentGameMode(GAME_MODE_MULTI_SERVER)
                            self.deployGamePass(self.test_gamepass) # deploy game pass
                            print("...init game pass...")
                            self.GameLoop()
                            print("...game pass over...")
                        elif int(ress) == 2:
                            ip_port = raw_input("\nInput Host IP:Port >>").split(':') # rs is a tuple
                            print("...setting network...")
                            self.setNetworkAddr((ip_port[0], int(ip_port[1])))
                            print("...network ready...")
                            self.setCurrentGameMode(GAME_MODE_MULTI_CLIENT)
                            print("...init game pass...")
                            self.ClientGameLoop()
                            print("...game pass over...")
                        else:
                            pass
                elif int(res) == 3:
                    ip_port = raw_input('Input HTTP Host:Port >>').split(':')
                    self.setHTTPHost((ip_port[0], int(ip_port[1])))
                    print('HTTP Host Change To ', ip_port)
                else:
                    break
            except Exception, e:
                print("Menu Loop Failed ==>", e)
        # self.ClientGameLoop()
        # get into main Menu
        # get into single-player mode
        # get into multi-player mode
        # play
        self.quit()


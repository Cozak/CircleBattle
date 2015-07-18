from CoSource import *
# under changer of the simulation world
class CoPhyWorld:
    def __init__(self):
        self.b2dworld = world(gravity=(0,0), doSleep=True)
        self.game_entities = [{}, {}, {}, {}, {}, {}] # player, enemy, wall, gun, bullet, diedbody
        self.renderInfoList = [[[], [], [], [], [], []],
                               [[], [], [], [], [], []],
                               [[], [], [], [], [], []],
                               [[], [], [], [], [], []]]    # may store multi-groups' info
        self.controller = None
        self.player_local_pos = [(0, 0), (0, 0), (0, 0), (0, 0)]    # in phy meter, four player only
        self.raycast_callback = None
        self.entity_filter_generator = None
    def registeFilterGenerator(self, entity_filter_generator):
        if entity_filter_generator:
            self.entity_filter_generator = entity_filter_generator
    def setPhyController(self, controller):
        if controller:
            self.controller = controller
    def updateViewPoint(self):
        all_player_mouse_pos = [self.controller.getMousePos(pid) for pid in COPLAYERLIST]
        for player in self.game_entities[COPLAYER].values():
            player_id = player.getPlayerID()
            if all_player_mouse_pos[player_id]:
                world_pos = player.getEntityPosition()
                self.player_local_pos[player.getPlayerID()] = ((VIEW_SCALA*(all_player_mouse_pos[player_id][0]
                                                                -SCREENWH[0]/2)+PPM*world_pos[0])/PPM,
                                                                (VIEW_SCALA*(SCREENWH[1]/2
                                                                -all_player_mouse_pos[player_id][1])+PPM*world_pos[1])/PPM)
    def getViewPoint(self):    # get the view point
        return self.player_local_pos
    # def setIncPlayerViewPos(self, playerid, posx, posy):
    #     self.player_local_pos[playerid][0] += posx
    #     self.player_local_pos[playerid][1] += posy
    def updateAllEntity(self):    # update every entity in this game system
        for body in self.b2dworld.bodies:
            body.userData['self'].process()
    def worldStep(self):
        self.b2dworld.Step(TIME_STEP, VELOCITY_ITER, POSITION_ITER)
    def collectEntityRenderInfo(self):
        render_filter = self.entity_filter_generator()
        for body in self.b2dworld.bodies:
            body.userData['self'].exportRenderInfo(self.renderInfoList, render_filter)
    def exportGroupsRenderInfo(self):
        self.updateViewPoint()
        self.collectEntityRenderInfo()
        return self.renderInfoList
    def clearGroupRenderInfo(self):
        for player_id in COPLAYERLIST: # clear old info
            # self.player_local_pos[player_id] = (0, 0)
            for tid in xrange(len(self.renderInfoList[player_id])):
                self.renderInfoList[player_id][tid] = []
    def addEntityToPhy(self, entity):
        self.game_entities[entity.COTYPE][entity.entity_id] = entity
    def destroyEntity(self, entity):
        if entity.mybody:
            self.b2dworld.DestroyBody(entity.mybody)
            self.game_entities[entity.COTYPE].pop(entity.entity_id, None)
    def clearPhyWorld(self):
        if self.game_entities:
            for dt in self.game_entities:
                for k,v in dt.items():
                    self.destroyEntity(v)
    def quit(self):
        pass
    def getPlayersList(self): # Update, must be synchronized
        return self.game_entities[COPLAYER].values()
    def getGunsList(self): # Update, must be synchronized
        return self.game_entities[COGUN].values()
    def getSeeAndHear(self, pos): # return the fixture of those entities detected
        if self.raycast_callback:
            ray_lists = []
            ray_normals = []
            ray_angel = 0.0
            while ray_angel < 360.0:
                self.raycast_callback.reset()
                end_point = (pos.x+self.raycast_callback.rad_length*math.sin(ray_angel),
                             pos.y+self.raycast_callback.rad_length*math.cos(ray_angel))
                self.b2dworld.RayCast(self.raycast_callback, pos, end_point)
                ray_lists.append(self.raycast_callback.points)    
                ray_normals.append(self.raycast_callback.normal)
                ray_angel += self.raycast_callback.rad_diff
            return ray_lists, ray_normals
        return None, None
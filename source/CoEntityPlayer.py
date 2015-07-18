from CoSource import *
from CoEntityPerson import *
from CoEntityDiedBody import *

class CoPlayer(CoPerson):
    COTYPE = COPLAYER
    COOFFSET = pygame.math.Vector2((ENTITY_OFFSET[COPLAYER][0]/PPM, ENTITY_OFFSET[COPLAYER][1]/PPM))
    def __init__(self, phyworld, center, player_id):
        CoPerson.__init__(self, phyworld, center)
        self.player_id = player_id
        self.mybody.CreateCircleFixture(radius=ENTITY_SHAPE[COPLAYER], density=1, friction=0)
        self.myimage = COPLAYER
        self.shift_len = ENTITY_SHIFT[COPLAYER]
        self.alliance = ALLIANCE_TEAMA
        self.speed = 7
        self.hp = 100
    def getPlayerID(self):
        return self.player_id
    def walk(self, dest):    # override
        CoPerson.walk(self, dest)
        if dest[0] == 0 and dest[1] == 0:
            self.image_idx = (AM_COPLAYER_UP if self.image_idx == AM_COPLAYER_DOWN else AM_COPLAYER_DOWN)
        else:
            self.image_idx = (AM_COPLAYER_RUNLONG if self.image_idx == AM_COPLAYER_RUNSHORT else AM_COPLAYER_RUNSHORT)
    def getAngleFromMouse(self, mouse_pos):
        return 0.0-STD_NORTH_VECTOR.angle_to((
            mouse_pos[0]-SCREENWH[0]/2, SCREENWH[1]/2-mouse_pos[1]))
    def process(self):
        CoPerson.process(self)
        mouse_pos = self.myworld.controller.getMousePos(self.player_id)
        mouse_pressed = self.myworld.controller.getMousePress(self.player_id)
        key_pressed = self.myworld.controller.getKeyPress(self.player_id)
        # # update Player Position
        # self.myworld.setIncPlayerViewPos(self.player_id, self.mybody.position.x, self.mybody.position.y)   # update view point
        # update based on the mouse position
        if mouse_pos:
            self.rotateToolAndPointTo(self.getAngleFromMouse(mouse_pos))
            self.front_back = (0 if mouse_pos[0] > SCREENWH[0]/2 else 1)
        if self.tool_entity:
            self.tool_entity.setFrontBack(self.front_back)
        posx, posy = 0, 0
        if key_pressed:
            if key_pressed[K_w]:    # Walk
                posy += 1
            elif key_pressed[K_s]:
                posy -= 1
            if key_pressed[K_a]:
                posx -= 1
            elif key_pressed[K_d]:
                posx += 1
            self.walk((posx, posy))
            if key_pressed[K_e]:
                self.detectAndTakeTools()
        if mouse_pressed and mouse_pressed[0]:    # left-fire
            self.justFire()
        else:
            self.refire()
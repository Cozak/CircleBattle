from CoSource import *
from CoEntityPerson import *
from CoEntityDiedBody import *

class CoEnemy(CoPerson):
    COTYPE = COENEMY
    COOFFSET = pygame.math.Vector2((ENTITY_OFFSET[COENEMY][0]/PPM, ENTITY_OFFSET[COENEMY][1]/PPM))
    def __init__(self, phyworld, center):
        CoPerson.__init__(self, phyworld, center)
        self.mybody.CreateCircleFixture(radius=ENTITY_SHAPE[COENEMY], density=1, friction=0)
        self.myimage = COENEMY
        self.shift_len = ENTITY_SHIFT[COENEMY]
        self.alliance = ALLIANCE_TEAMB
        self.hp = 100
        self.speed = 6
        self.state_machine = None # their brains
    def setStateMachine(self, smc):
        self.state_machine = smc
    def getAngleFromWorld(self, raw_pos):
        return 0.0-STD_NORTH_VECTOR.angle_to((
                raw_pos[0]-self.mybody.position.x, raw_pos[1]-self.mybody.position.y))
    def process(self):
        CoPerson.process(self) # check whether is died
        actions = self.think()
        if actions:
            if actions[0] == 2:
                self.rotateToolAndPointTo(self.getAngleFromWorld((actions[1].x, actions[1].y)))
                self.front_back = (0 if actions[1].x > self.mybody.position.x else 1)
                if self.tool_entity:
                    self.tool_entity.setFrontBack(self.front_back)
                self.justFire()
                if (actions[1]-self.mybody.position).Normalize() > ENEMY_SROUND/PPM:
                    self.walk((actions[1].x-self.mybody.position.x, actions[1].y-self.mybody.position.y))
                else:
                    self.walk((Random.randint(-1, 1), Random.randint(-1, 1)))
            else:
                if actions[0] == 1: # try to take a weapon
                    self.detectAndTakeTools()
                self.walk((actions[1], actions[2]))
    def walk(self, dest):    # override
        CoPerson.walk(self, dest)
        if dest[0] == 0 and dest[1] == 0:
            self.image_idx = (AM_COENEMY_UP if self.image_idx == AM_COENEMY_DOWN else AM_COENEMY_DOWN)
        else:
            self.image_idx = (AM_COENEMY_RUNLONG if self.image_idx == AM_COENEMY_RUNSHORT else AM_COENEMY_RUNSHORT)
    def think(self): # use their brain
        if not self.state_machine:
            return None
        if not self.tool_entity or self.tool_entity.checkRemainAmmo() <= 0: # lack of weapon
            new_tool = None; distance = FAR_TO_TAKE_TOOL*100/PPM
            for gun in self.myworld.getGunsList():
                if not gun.istaken:
                    dist = (gun.mybody.position - self.mybody.position).Normalize()
                    if dist < distance:
                        distance = dist
                        new_tool = gun
            return (1, new_tool.mybody.position.x - self.mybody.position.x,
             new_tool.mybody.position.y - self.mybody.position.y) if new_tool else (0,
                                         Random.randint(-1, 1), Random.randint(-1, 1))
        for player in self.myworld.getPlayersList():
            if (player.mybody.position-self.mybody.position).Normalize() < ENEMY_EYEVIEW/PPM:
                return (2, player.mybody.position)
        return (0, Random.randint(-1, 1), Random.randint(-1, 1))
    def preDied(self):
        CoPerson.preDied(self)
        angle = STD_NORTH_VECTOR.angle_to((self.mybody.linearVelocity.x, self.mybody.linearVelocity.y))
        CoDiedBody(self.myworld, self.getEntityPosition(), angle) # create its died body
from CoSource import *
from CoEntityBase import *

# Weapon
class CoWeapon(CoDynamicEntity):
    COFIREOFFSET = None # each kind of weapon may has its own fire_pos
    def __init__(self, phyworld, center):
        CoDynamicEntity.__init__(self, phyworld, center)
        self.istaken = False
        self.bullet_class = None    # which kinds of bullet this weapon can create, derived class
        self.myjoint = None
        self.myownner = None
        self.ammo = 1
    def tokenBy(self, person):
        self.myjoint = self.myworld.b2dworld.CreateRevoluteJoint(bodyA=person.mybody,
                                          bodyB=self.mybody,
                                          localAnchorA=(0, 0),
                                          localAnchorB=(0, 0), # center of tire
                                          enableMotor=False,
                                          maxMotorTorque=1000,
                                          enableLimit=False,
                                          lowerAngle=0,
                                          upperAngle=0,
                                          )
        self.mybody.fixtures[0].sensor = True    # sensor never take part in contact
        self.alliance = person.alliance
        self.istaken = True
        self.render_level = person.render_level
        self.rotateByAngle(person.image_rotate)
        self.myownner = person
    def dropBy(self):
        self.myownner = None
        self.myworld.b2dworld.DestroyJoint(self.myjoint) # release and destroy joint
        self.mybody.fixtures[0].sensor = False
        self.alliance = ALLIANCE_GOD
        self.istaken = False
        self.render_level = RENDERLEVEL_PACKET
        self.front_back = 0
        self.rotateByAngle(Random.randint(-180, 180))
        self.mybody.linearVelocity *= 0
        # if self.ammo <= 0: # destroy self
        #     self.hp = 0 # self destroied in process method
    def setFrontBack(self, yn):
        self.front_back = yn
    def rotateByAngle(self, angle):     # angle in degree
        self.image_rotate = angle   # set image angel
        self.mybody.angle = (0.0-angle)/360.0*math.pi   # set body angel in rad
    def fire(self): # create bullet
        pass
    def refire(self):
        pass
    def getCurrentAngle(self):
        return self.image_rotate
    def exportRenderInfo(self, renderList, render_filter):    # it can rotate when taken
        if self.istaken:
           return   # do nothing
        pos = (self.mybody.position.x, self.mybody.position.y)
        # drange = (self.shift_len*self.image_idx, 0, self.shift_len, IMAGES[self.myimage].get_height())
        encode_data = encodeRenderInfo(self.myimage, self.image_idx, int(self.image_rotate%360), self.front_back)
        for pid in render_filter(pos):
            renderList[pid][self.render_level].append((pos, encode_data))
    def exportWhenTaken(self, renderList, render_filter):    # its owner will call this method
            CoDynamicEntity.exportRenderInfo(self, renderList, render_filter)
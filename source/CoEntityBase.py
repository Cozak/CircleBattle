from CoSource import *

class CoGameEntity:
    ''' Base Class For Game Entity  '''
    COOFFSET = None
    def __init__(self, phyworld):
        self.entity_id = id(self)
        self.myworld = phyworld
        self.mybody = None
        self.myimage = None
        self.image_idx = 0
        self.shift_len = 0
        self.front_back = 0
        self.image_rotate = 0
        # self.std_vec = pygame.math.Vector2(0, 1)    # standard Vector Point to the North
        # self.image_frame = None
        self.render_level = 0
        self.current_state = []
        self.hp = 1
        self.alliance = ALLIANCE_GOD
        self.attach = []    # allow other entity move with its owner, these attachment are sensors
        self.myworld.addEntityToPhy(self)    # add self to the list of phyworld
    def exportRenderInfo(self, renderList, render_filter):        # derived class may override this method to deal with attachment
        tmpvec = self.COOFFSET.rotate(int(0.0-self.image_rotate))
        pos = (self.mybody.position.x + tmpvec.x, self.mybody.position.y + tmpvec.y)
        # drange = (self.shift_len*self.image_idx, 0, self.shift_len, IMAGES[self.myimage].get_height())
        encode_data = encodeRenderInfo(self.myimage, self.image_idx,
                                       int(self.image_rotate%360), self.front_back)
        for pid in render_filter(pos):
            renderList[pid][self.render_level].append((pos, encode_data))
    def process(self):    # should be override by the final derived class
        if self.hp <= 0:
            self.preDied()
            self.destroy()
    def updateAttachment(self):    # notify the attachment if sth change
        pass
    def changeHP(self, val):
        self.hp += val
    def getEntityPosition(self):
        return self.mybody.position.x, self.mybody.position.y
    def preDied(self):    # this method should be override if in need
        pass
    def destroy(self):
        if self.mybody and self.myworld:
            self.myworld.destroyEntity(self)

# Static Entity like wall and plant
class CoStaticEntity(CoGameEntity):
    '''  '''
    def __init__(self, phyworld, center):
        CoGameEntity.__init__(self, phyworld)
        self.mybody = phyworld.b2dworld.CreateStaticBody(position=center)
        self.mybody.userData = {}
        self.mybody.userData['self'] = self

# Dynamic Entity like player, gun, bullet
class CoDynamicEntity(CoGameEntity):
    def __init__(self, phyworld, center):
        CoGameEntity.__init__(self, phyworld)
        self.mybody = phyworld.b2dworld.CreateDynamicBody(position=center)
        self.mybody.userData = {}
        self.mybody.userData['self'] = self
        self.speed = 0    # times of speed vector
    def getLinearVelocity(self):
        return self.mybody.linearVelocity
    def setLinearVelocity(self, vec):    # vec is (a,b)
        self.mybody.linearVelocity.SetZero()
        self.mybody.linearVelocity += vec
    def setLinearForce(self, force):    # force is (a,b)
        self.mybody.ApplyForceToCenter(force)
    def applyLinearImpulse(self, impulse):    # impulse is (a, b)
        self.mybody.ApplyLinearImpulse(impulse, self.mybody.localCenter, True)
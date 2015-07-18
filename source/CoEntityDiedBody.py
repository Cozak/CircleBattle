from CoSource import *
from CoEntityBase import *

class CoDiedBody(CoDynamicEntity):
    COTYPE = CODIEDBODY
    COOFFSET = pygame.math.Vector2((ENTITY_OFFSET[CODIEDBODY][0]/PPM, ENTITY_OFFSET[CODIEDBODY][1]/PPM))
    def __init__(self, phyworld, center, angle):
        CoDynamicEntity.__init__(self, phyworld, center)
        self.mybody.CreateCircleFixture(radius=ENTITY_SHAPE[CODIEDBODY], density=1, friction=0, restitution=1.0)
        self.myimage = CODIEDBODY
        self.shift_len = ENTITY_SHIFT[COENEMY]
        self.image_idx = Random.randint(0, len(AM_CODIEDBODY_LIST)-1)
        self.render_level = RENDERLEVEL_PLANT
        self.shift_len = ENTITY_SHIFT[CODIEDBODY]
        self.image_rotate = angle
        self.speed = 24   # 30 times of stander vector
        self.hp = 1
    def process(self):
        CoDynamicEntity.process(self)
        if self.speed > 0:
            self.speed -= 4
        tpvec = STD_NORTH_VECTOR.rotate(int(0.0-self.image_rotate))*self.speed
        self.mybody.linearVelocity = tpvec
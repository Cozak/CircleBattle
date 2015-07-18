from CoSource import *
from CoEntityProperty import *
from CoEntityBase import *

class CoBullet(CoDynamicEntity, CoHurtfull):
    COTYPE = COBULLET
    COOFFSET = pygame.math.Vector2((ENTITY_OFFSET[COBULLET][0]/PPM, ENTITY_OFFSET[COBULLET][1]/PPM))
    # COOOOT = 0
    def __init__(self, phyworld, center, angle):
        CoDynamicEntity.__init__(self, phyworld, center)
        CoHurtfull.__init__(self, -4)
        self.mybody.CreateCircleFixture(radius=ENTITY_SHAPE[COBULLET], density=1, friction=0, restitution=1.0)
        self.myimage = COBULLET
        self.render_level = RENDERLEVEL_BULLET
        self.shift_len = ENTITY_SHIFT[COBULLET]
        self.speed = 20   # 30 times of stander vector
        self.image_rotate = angle
        tpvec = STD_NORTH_VECTOR.rotate(int(0.0-self.image_rotate))*self.speed
        self.mybody.linearVelocity = tpvec
        # self.mybody.ApplyLinearImpulse(impulse=(tpvec.x, tpvec.y), point=self.mybody.position, wake=True)
        self.hp = 30
        # CoBullet.COOOOT += 1
        # print("Total Bullet: %d" % (CoBullet.COOOOT))
    def hurt(self, entity):    # when hit sth, a bullet may reflect or disappear
        if self.alliance != entity.alliance:    # this kind of bullet won't hurt alliance
            CoHurtfull.hurt(self, entity)
        self.hp *= 0.2
        # self.preDied()    # release some smoke
        # self.destroy()    # bullet disappear
    def adjustAngle(self):
        vec = (self.mybody.linearVelocity.x, self.mybody.linearVelocity.y)
        self.image_rotate = 0.0-STD_NORTH_VECTOR.angle_to(vec)
    def process(self):
        self.adjustAngle() # adjust self angle
        self.hp -= 1
        CoDynamicEntity.process(self)
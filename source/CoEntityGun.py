from CoSource import *
from CoEntityWeapon import *
from CoEntityBullet import *

class CoGun(CoWeapon):
    COTYPE = COGUN
    COOFFSET = pygame.math.Vector2((ENTITY_OFFSET[COGUN][0]/PPM, ENTITY_OFFSET[COGUN][1]/PPM))
    COFIREOFFSET = COOFFSET*2
    def __init__(self, phyworld, center):
        CoWeapon.__init__(self, phyworld, center)
        self.mybody.CreatePolygonFixture(box=ENTITY_SHAPE[COGUN])
        self.myimage = COGUN
        self.render_level = RENDERLEVEL_PACKET
        self.shift_len = ENTITY_SHIFT[COGUN]
        self.bullet_class = CoBullet    # type of bullet
        self.ammo = 100
        self.fire_diff = 6
        self.fire_down = 0
    def setGunAttr(self, ammo=100, diff=5):
        if ammo > 0:
            self.ammo = ammo
        if diff > 0:
            self.fire_diff = diff
    def refire(self):
        self.fire_down = 0
    def fire(self): # create bullet
        if self.myownner and not self.fire_down and self.ammo > 0:
            fpos = self.COFIREOFFSET.rotate(int(0.0-self.image_rotate))
            self.bullet_class(self.myworld, (fpos.x+self.myownner.mybody.position.x,
                                            fpos.y+self.myownner.mybody.position.y),
                                            self.image_rotate).alliance = self.alliance
            self.ammo -= 1
            self.fire_down = self.fire_diff
        self.fire_down -= 1
    def dropBy(self):
        CoWeapon.dropBy(self)
        if self.ammo <= 0: # destroy self
            self.hp = 0 # self destroied in process method
    def checkRemainAmmo(self):
        return self.ammo
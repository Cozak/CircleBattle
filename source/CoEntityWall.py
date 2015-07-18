from CoSource import *
from CoEntityBase import *

# Entity Wall in Game
class CoWall(CoStaticEntity):
    COTYPE = COWALL
    COOFFSET = pygame.math.Vector2((ENTITY_OFFSET[COWALL][0]/PPM, ENTITY_OFFSET[COWALL][1]/PPM))
    def __init__(self, phyworld, center):
        CoStaticEntity.__init__(self, phyworld, center)
        self.mybody.CreatePolygonFixture(box=ENTITY_SHAPE[COWALL])
        self.myimage = COWALL
        self.render_level = RENDERLEVEL_TOP
        self.shift_len = ENTITY_SHIFT[COWALL]
        # self.image_frame = [self.shift_len*self.image_idx, 0, self.shift_len, self.myimage.get_height]
        self.hp = 300
    def changeHP(self, hp):
        # change state based on the HP
        CoStaticEntity.changeHP(self, hp)
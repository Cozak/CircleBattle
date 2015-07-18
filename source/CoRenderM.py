from CoSource import *
from CoGameM import *
# Render Work here, for local player only
class CoRender:
    def __init__(self, screen):
        # tolerate range for objects displayed in sight
        self.tolerateWH = TOLERANCE_RANGE    
        self.screen = screen
        self.screenWH = (screen.get_width(),
                         screen.get_height())
        self.display_range = (float(self.tolerateWH[0]+self.screenWH[0]/2)/PPM,
                             float(self.tolerateWH[1]+self.screenWH[1]/2)/PPM)
        # choose game objects and display them if insight
        self.cur_render_origin = (0,0)
    # encode_data format (pos, encode_data)    
    # obj format (pos, img, (ix, iy, w, h), angle, front_back), pos is the center of the image
    def renderProcessor(self, objmultigroups):    
        self.screen.fill((0, 0, 0))
        for objgroups in objmultigroups:
            for obj in objgroups:
                # if self.isInSight((obj[0][0]*PPM, obj[0][1]*PPM)):
                # decode and restore the encode_data
                decode_data = decodeRenderInfo(obj[1])
                # drange = (self.shift_len*self.image_idx, 0, self.shift_len, IMAGES[self.myimage].get_height())
                drange = (ENTITY_SHIFT[decode_data[0]]*decode_data[1], 0, ENTITY_SHIFT[decode_data[0]], IMAGES[decode_data[0]].get_height())
                tmp_image = IMAGES[decode_data[0]].subsurface(drange)
                if decode_data[3]:    # flip the image if marked
                    tmp_image = pygame.transform.flip(tmp_image, True, False)
                # be careful, pygame take ccw as default
                tmp_image = pygame.transform.rotate(tmp_image, 0.0-decode_data[2])  
                self.renderBlit(tmp_image, (self.screenWH[0]/2-
                                    (self.cur_render_origin[0]
                                    -obj[0][0])*PPM-tmp_image.get_width()/2,
                                    self.screenWH[1]/2+(self.cur_render_origin[1]-obj[0][1])*PPM
                                    -tmp_image.get_height()/2))
                # self.screen.blit(tmp, (obj[0][0]*PPM-tmp.get_width()/2, self.screenWH[1]-(obj[0][1]*PPM+tmp.get_height()/2)))
    def renderBlit(self, image, pos):
        self.screen.blit(image, pos)
    def renderDisplay(self):
        pygame.display.flip()
    def updateRenderOrigin(self, view_center): # in meters, the center of viewpos in phyworld
        if view_center:
            self.cur_render_origin = view_center
    def isInSight(self, entity_pos, view_center):    # all in meters
        dx, dy = math.fabs(entity_pos[0]-view_center[0]), math.fabs(entity_pos[1]-view_center[1])
        return dx <= self.display_range[0] and dy <= self.display_range[1]
    # pos should the position of the screen-center
    # def updateRenderOrigin(self, player_pos, mouse_pos):        
    #     self.cur_render_origin = (VIEW_SCALA*(mouse_pos[0]
    #                             -self.screenWH[0]/2)+PPM*player_pos[0],
    #                             VIEW_SCALA*(self.screenWH[1]/2
    #                             -mouse_pos[1])+PPM*player_pos[1])
    # def isInSight(self, pos):    # all in pixels, pos is the center of the image
    #     dx, dy = math.fabs(pos[0]-self.cur_render_origin[0]), math.fabs(pos[1]-self.cur_render_origin[1])
    #     return dx <= self.display_range[0] and dy <= self.display_range[1]
    def quit(self):
        pass
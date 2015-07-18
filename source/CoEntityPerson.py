from CoSource import *
from CoEntityBase import *

# Entity looks like an actor
class CoPerson(CoDynamicEntity):
    def __init__(self, phyworld, center):
        CoDynamicEntity.__init__(self, phyworld, center)
        self.tool_entity = None    # person can take weapon
        self.render_level = RENDERLEVEL_PERSON
    def setPersonAttr(self, hp=100, speed=7):
        if hp > 0:
            self.hp = hp
        if speed >= 0:
            self.speed = speed
    def rotateToolAndPointTo(self, angle):    # angle based on the North Vector
        if self.tool_entity:
            self.tool_entity.rotateByAngle(angle)
    def detectAndTakeTools(self): # if these any weapon around, take one of them randomly
        guns = self.myworld.getGunsList() # call world api to get the closed one
        new_tool = None;distance = FAR_TO_TAKE_TOOL/PPM
        for gun in guns:
            if not gun.istaken and gun.ammo > 0:
                dist = (gun.mybody.position - self.mybody.position).Normalize()
                if dist < distance:
                    distance = dist
                    new_tool = gun
        self.changeTool(new_tool)
    def changeTool(self, tool):    # change tool, single weapon for test
        if self.tool_entity:   # drop old weapon
            self.tool_entity.dropBy()
            self.tool_entity = None
        self.tool_entity = tool
        if tool:
            self.tool_entity.tokenBy(self) # notify the weapon about its new ownner
    def justFire(self):    # call the weapon to attack
        if self.tool_entity:
            self.tool_entity.fire()
    def refire(self):
        if self.tool_entity:
            self.tool_entity.refire()
    def think(self):
        pass
    def walk(self, destination):    # destination is (x, y)
        vec = Box2D.b2Vec2(destination)
        vec *= (self.speed/vec.Normalize() if vec.Normalize() != 0 else self.speed)
        self.mybody.linearVelocity = vec
    def exportRenderInfo(self, renderList, render_filter): # person may have weapons
        if self.tool_entity:
            cur_angle = self.tool_entity.getCurrentAngle() % 360
            if cur_angle <= 90.0 or cur_angle >= 270.0:
                self.tool_entity.exportWhenTaken(renderList, render_filter)
                CoDynamicEntity.exportRenderInfo(self, renderList, render_filter) # render its own info
            else:
                CoDynamicEntity.exportRenderInfo(self, renderList, render_filter) # render its own info
                self.tool_entity.exportWhenTaken(renderList, render_filter)
            return
        CoDynamicEntity.exportRenderInfo(self, renderList, render_filter) # render its own info
    def preDied(self):
        if self.tool_entity: # if has weapon, drop it
            self.tool_entity.dropBy()

from CoSource import *
from CoEntityProperty import *
# from CoGameEntity import *

# Collide Listener and Filter
class CoCollidListener(Box2D.b2ContactListener):
    def BeginContact(self, contact):
        Box2D.b2ContactListener.BeginContact(self, contact)
    def EndContact(self, contact):
        Box2D.b2ContactListener.EndContact(self, contact)
    def PostSolve(self, contact, impulse):
        entityA = contact.fixtureA.body.userData['self']
        entityB = contact.fixtureB.body.userData['self']
        if isinstance(entityA, CoHurtfull):
            entityA.hurt(entityB)
        if isinstance(entityB, CoHurtfull):
            entityB.hurt(entityA)
    def PreSolve(self, contact, oldManifold):
        Box2D.b2ContactListener.PreSolve(self, contact, oldManifold)
        pass

class CoCollidFilter(Box2D.b2ContactFilter):
    def ShouldCollide(self, fixtureA, fixtureB):
        entityA = fixtureA.body.userData['self']
        entityB = fixtureB.body.userData['self']
        if entityB.COTYPE in COLLIDE_FILTER_TABLE[entityA.COTYPE]:
            return False
        # for special collide event
        # kick away guns
        return True

# RayCast Callback
class RayCastMultipleCallback(Box2D.b2RayCastCallback):
    """This raycast collects multiple hits."""
    def __init__(self, **kwargs):
        Box2D.b2RayCastCallback.__init__(self, **kwargs)
        self.points=[]
        self.normal = None
        self.rad_diff = 6. # interval between two rays, must be passtive number
        self.rad_length = VIEW_RANGE / PPM # in meters
    def reset(self):
        self.points = []
        self.normal = None
    def ReportFixture(self, fixture, point, normal, fraction):
        self.points.append(Box2D.b2Vec2(point))
        if not self.normal:
            self.normal = normal
        return 1.0
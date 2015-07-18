from CoSource import *
# Hurtfull
class CoHurtfull:
    def __init__(self, damage):
        self.damage_val = damage
    def hurt(self, entity):        # override and add extra method
        entity.changeHP(self.damage_val)

# whether this entity can be heared
class CoHearable:
    def __init__(self):
        self.alert = False
# add walls
for i in xrange(80):
    CoWall(phyworld, (i*2-80, 60))
    CoWall(phyworld, (i*2-80, -60))
for j in xrange(59):
    CoWall(phyworld, (-80, 58-j*2))
    CoWall(phyworld, (80, 58-j*2))
for k in xrange(20):
    CoWall(phyworld, (Random.randint(-60, 60), Random.randint(-50, 10)))
# add a player
gun0 = CoGun(phyworld, (0, 0))
gun0.setGunAttr(diff=2, ammo=400) # set Gun Attr
player_0 = CoPlayer(phyworld, (70, 0), COPLAY_0)
player_0.setPersonAttr(hp=20000, speed=10)
player_0.changeTool(gun0)

gun1 = CoGun(phyworld, (0, 0))
player_1 = CoPlayer(phyworld, (70, 5), COPLAY_1)
player_1.setPersonAttr(hp=20000, speed=10)
player_1.changeTool(gun1)

# gun2 = CoGun(phyworld, (0, 0))
# player_2 = CoPlayer(phyworld, (70, -5), COPLAY_2)
# player_2.setPersonAttr(hp=200000, speed=10)
# player_2.changeTool(gun2)

# gun3 = CoGun(phyworld, (0, 0))
# player_3 = CoPlayer(phyworld, (65, 0), COPLAY_3)
# player_3.setPersonAttr(hp=200000, speed=10)
# player_3.changeTool(gun3)
# enemys
for i in xrange(100):
    gune = CoGun(phyworld, (0, 0))
    gune.setGunAttr(ammo=100, diff=6)
    enemy1 = CoEnemy(phyworld, (-50-i, i))
    enemy1.setStateMachine(self.local_state_machine)
    enemy1.setPersonAttr(hp=20, speed=5) # set ememy attr
    enemy1.changeTool(gune)

for i in xrange(20):
    gunm = CoGun(phyworld, (Random.randint(-60, 60), Random.randint(20, 50)))
    gune.setGunAttr(ammo=100, diff=6)
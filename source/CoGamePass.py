from CoSource import *
from CoGameEntity import *
# design and deploy the map of a pass of the game
class CoGamePass:
    def __init__(self):
        self.local_state_machine = None
    def setStateMachine(self, sm):
        self.local_state_machine = sm
    def deploy(self, phyworld):
        try:
            with open("GamePass.py") as fin:
                try:
                    code = fin.read()
                    exec(code)
                except Exception, e:
                    print("Game Pass Deploy Error ", e)
        except:
            print("Can't find GamePass.py")
        
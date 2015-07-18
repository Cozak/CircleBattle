from CoSource import *
# different kind of entity has different state-machine
class CoStateMachine:
    def __init__(self):
        self.state_machines = {COENEMY:self.enemySM}
    def runStateMachine(self, ai_type, cur_state, feels):    # entrance
        self.state_machines[ai_type](cur_state, feels)
    # cur_state = [fight : 0/1, avoid : 0/1]
    # feels = [target : 0/1]
    def enemySM(self, cur_state, feels):
        if feels[0] == 0:    # no target
            cur_state[0], cur_state[1] = 0, 0
        elif feels[0] == 1:    # see target
            cur_state[0], cur_state[1] = 1, 1
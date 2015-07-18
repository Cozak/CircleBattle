from CoSource import *
# command all found here
class CoController:
    def __init__(self):
        self.local_player_id = COPLAY_0
        self.player_order_info = {}
    # def setLocalPlayerID(self, player_id):
    #     self.local_player_id = player_id
    def updateLocalController(self): # sys must call this function and update those command
        pygame.event.get()
        self.player_order_info[self.local_player_id] = (pygame.mouse.get_pos(),
                                                        pygame.mouse.get_pressed(),
                                                        pygame.key.get_pressed())
    def updateControllerFromNetwork(self, player_info): # update tel-command from other player
        # update entityTable here
        self.player_order_info[player_info[0]] = player_info[1]
    def getKeyPress(self, player_id):
        try:
            return self.player_order_info[player_id][2]
        except:
            return None
    def getMousePos(self, player_id):
        try:
            return self.player_order_info[player_id][0]
        except:
            return None
    def getMousePress(self, player_id):
        try:
            return self.player_order_info[player_id][1]
        except:
            return None
    def updateMenuCommand(self, data):
        pass
    def clearControllor(self):
        self.player_order_info.clear()
    def quit(self):
        pass
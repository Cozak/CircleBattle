from __future__ import print_function

# Game Main System
from CoGameM import *

# main
if __name__ == '__main__':
    # additional model
    from CoStateMachine import *
    from CoGameEntity import *
    from CoGamePass import *
    from CoDataCollector import *
    # Injection of Data Collection in AOP Style
    data_collector = CoDataCollector()
    data_collector.inject()
    # =================================
    n_listener = CoCollidListener()
    n_filter = CoCollidFilter()
    n_callback = RayCastMultipleCallback()
    smh = CoStateMachine()    # state-machine
    gpass = CoGamePass()    # game pass 1
    gpass.setStateMachine(smh) # load a state-machine
    print("Sys: Init Finished")
    game = CoGame()
    print("Sys: Game Init Finished")
    game.setCollidListener(n_listener)
    game.setCollidFilter(n_filter)
    game.setRayCastCallback(n_callback)
    game.setDataCollector(data_collector)
    print("Sys: Ready For Pass")
    # game.deployGamePass(gpass)
    game.setTestGamePass(gpass)
    print("Sys: Deploy Pass Finished")
    # -----------------------------
    # GAME_MODE_DEFAULT, GAME_MODE_SINGLE, GAME_MODE_MULTI_CLIENT, GAME_MODE_MULTI_SERVER
    # game.setCurrentGameMode(GAME_MODE_SINGLE)
    # game.setLocalPlayerID(COPLAY_0)
    # --------- HTTP Server -------
    game.setHTTPHost(HTTP_ADDR)
    # -----------------------------
    game.ALLStart()
    pygame.quit()
    raw_input("Any Press To Exit...")

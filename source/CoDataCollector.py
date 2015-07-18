# -*- coding:UTF-8 -*-
import json, time, copy
from CoGamePass import  CoGamePass
from CoPhyWorldM import *
from CoGameM import *
from CoGameEntity import CoPlayer
from CoGameEntity import CoEnemy
# For Game Data Collector
class CoDataCollector:
    def __init__(self):
        self.data = {"game_timer" : "not set yet",
                          "submit_time" : None, 
                          "pass_name" : "pass1",
                          "pass_timer" : None,
                          "pass_over_timer": None,
                          "trace" : [],
                          "ammo_consumption": 0,
                          "number_of_hit": 0,
                          "injurt_value" : 0
                          }
        self.data_backup = copy.deepcopy(self.data)
        self.is_ready = False
        
    def isReady(self):
        return self.is_ready
        
    def getUploadData(self):
        self.data["submit_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        upload_data = {'operation' : 'add' ,
                               'database_name': 'circle-battle', 
                               'collection_name': 'test_collection1',
                               'documents' :  json.dumps([self.data])}
        self.data = copy.deepcopy(self.data_backup)
        self.is_ready = False
        return upload_data
        
    def injectDataFront(self, *arg, **kwargs):
        print('Record Something')
        
    def decorateFuncWithArgs(self, oldfunc, 
                    front_injection_func = None,
                    back_injection_func = None): # 对原始函数进行数据记录注入，oldfunc为原始方法
        def newfunc(*arg, **kwargs):
                if front_injection_func:
                        front_injection_func(*arg, **kwargs)
                res = oldfunc(*arg, **kwargs)
                if back_injection_func:
                        back_injection_func(*arg, **kwargs)
                return res
        return newfunc
    def decorateFuncWithNoArgs(self, oldfunc, 
                    front_injection_func = None,
                    back_injection_func = None): # 对原始函数进行数据记录注入，oldfunc为原始方法
        def newfunc(*arg, **kwargs):
                if front_injection_func:
                        front_injection_func()
                res = oldfunc(*arg, **kwargs)
                if back_injection_func:
                        back_injection_func()
                return res
        return newfunc
        
    #decorate the CoGame.__init__(self) function
    def startGameTiming(self):
        #self.data["game_timer"] = time.clock()
        pass
        
    #decorate the CoGame.quit(self) function    
    def endGameTiming(self):
        #self.data["game_timer"] = int(time.clock() - self.data["game_timer"])
        pass
    
    #decorate the CoGamePass.deploy(self, phyworld) function
    def startPassTiming(self):
        self.data["pass_timer"] = time.clock()
    
    #decorate the CoGame.GameLoop(self) function
    def endPassTiming(self):
        self.data["pass_timer"] = int(time.clock() - self.data["pass_timer"])
        
    #decorate the CoGamePass.deploy(self, phyworld) function
    def startPassOverTiming(self):
        self.data["pass_over_timer"] = time.clock()
        
    #decorate the CoGame.GameLoop(self)  function
    def endPassOverTiming(self):
        self.data["pass_over_timer"] = int(time.clock() - self.data["pass_over_timer"])
        self.is_ready = True
    
    #decorate the CoPhyWorld.setViewPoint(self, playerid, posx, posy) function
    def recordTrace(self, *arg, **kwargs):
        #self.data["trace"].append((arg[2], arg[3]))
        pass
        
    #decorate the CoPlayer.justFire(self)  function
    def recordAmmoConsumption(self):
        self.data["ammo_consumption"] += 1

    #decorate the CoEnemy.changeHP(self, value)
    def recordNumberOfHit(self):
        self.data["number_of_hit"] += 1
        
    #decorate the CoPlayer.changeHP(self, value)
    def recordInjurtValue(self, *arg, **kwargs):
        self.data["injurt_value"] += arg[1]
        
        
    def inject(self):
        CoGame.__init__ = self.decorateFuncWithNoArgs(CoGame.__init__, self.startGameTiming)
        CoGame.quit = self.decorateFuncWithNoArgs(CoGame.quit, self.endGameTiming)
        CoGamePass.deploy = self.decorateFuncWithNoArgs(CoGamePass.deploy, self.startPassTiming)
        CoGame.GameLoop = self.decorateFuncWithNoArgs(CoGame.GameLoop, None, self.endPassTiming)
        CoGamePass.deploy = self.decorateFuncWithNoArgs(CoGamePass.deploy, self.startPassOverTiming)
        CoGame.GameLoop = self.decorateFuncWithNoArgs(CoGame.GameLoop, None, self.endPassOverTiming)
        # CoPhyWorld.setViewPoint = self.decorateFuncWithArgs(CoPhyWorld.setViewPoint, self.recordTrace)
        CoPlayer.justFire = self.decorateFuncWithNoArgs(CoPlayer.justFire, self.recordAmmoConsumption)
        CoEnemy.changeHP = self.decorateFuncWithNoArgs(CoEnemy.changeHP, self.recordNumberOfHit)
        CoPlayer.changeHP = self.decorateFuncWithArgs(CoPlayer.changeHP, self.recordInjurtValue)
    
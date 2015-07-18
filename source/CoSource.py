from __future__ import print_function
import pygame, Box2D, math, os, sys, pickle, threading
import socket, select, httplib, urllib
from pygame.locals import *
from Box2D.b2 import *
import random as Random
import time as Time

# Game System
SCREENWH = (960, 600)
TOLERANCE_RANGE = (200, 200)
VIEW_SCALA = 0.4
PPM = 30.0     # pixels per meter
TARGET_FPS = 20
HTTP_FPS = 5
SERVER_FPS = 60
TIME_STEP = 1.0/TARGET_FPS
VELOCITY_ITER = 10
POSITION_ITER = 10
RENDER_QUEUE_SIZE = 2
GAME_MODE_DEFAULT, GAME_MODE_SINGLE, GAME_MODE_MULTI_CLIENT, GAME_MODE_MULTI_SERVER = 0, 1, 2, 3
# About Range
FAR_TO_TAKE_TOOL = 50 # in pixels
ENEMY_EYEVIEW = 800 # in pixels
ENEMY_SROUND = 400 # in pixels
VIEW_RANGE = 800 # in pixels
# Common Identity
COLORKEY = (255,255,255)
ALLIANCE_GOD = 0;ALLIANCE_TEAMA=1;ALLIANCE_TEAMB=2;ALLIANCE_TEAMC=3     # belongs to different team
RENDERLEVEL_GROUND=0;RENDERLEVEL_PLANT=1;RENDERLEVEL_PACKET=2
RENDERLEVEL_PERSON=3;RENDERLEVEL_BULLET=4;RENDERLEVEL_TOP=5
RENDERLEVEL = (RENDERLEVEL_GROUND,RENDERLEVEL_PLANT,
                RENDERLEVEL_PACKET,RENDERLEVEL_PERSON,
                RENDERLEVEL_BULLET,RENDERLEVEL_TOP)
# About Entity
COPLAYER_MEUN_DIFF = 100
COPLAY_0=0;COPLAY_1=1;COPLAY_2=2;COPLAY_3=3     # multi-player code, four player only
COPLAYERLIST = [COPLAY_0, COPLAY_1, COPLAY_2, COPLAY_3]
COPLAYER=0;COENEMY=1;COWALL=2;COGUN=3;COBULLET=4;CODIEDBODY=5
# Entity Animation
AM_COPLAYER_UP=0;AM_COPLAYER_DOWN=1;AM_COPLAYER_RUNLONG=2;AM_COPLAYER_RUNSHORT=3;
AM_COENEMY_UP=0;AM_COENEMY_DOWN=1;AM_COENEMY_RUNLONG=2;AM_COENEMY_RUNSHORT=3;
AM_CODIEDBODY_LIST = (0, 1, 2, 3)
# Filter table
COLLIDE_FILTER_TABLE = {COPLAYER:[COPLAYER, COENEMY, COGUN, CODIEDBODY],
                        COENEMY:[COPLAYER, COENEMY, COGUN, CODIEDBODY],
                        COWALL:[COWALL], 
                        COGUN:[COGUN, COBULLET, COPLAYER, COENEMY, CODIEDBODY], 
                        COBULLET:[COGUN, COBULLET, CODIEDBODY],
                        CODIEDBODY:[COGUN, COBULLET, COPLAYER, COENEMY, CODIEDBODY]}
# Image Source And Absolute Entity
ENTITY_TYPE = (COPLAYER,COENEMY,COWALL,COGUN,COBULLET,CODIEDBODY)
ENTITY_SHAPE = (1, 1, (0.7, 0.7), (0.4, 0.4), 0.1, 0.1)    # in pixels
ENTITY_OFFSET = ((0, 0), (0, 0), (0, 0), (0, 30), (0, -0.5), (0, 0))    # in pixels
ENTITY_SHIFT = (35, 35, 60, 30, 5, 35)        # shift is nonzero, which means that the entity has animations

# NetWork and Server
COMULTIPLAYER_NUM = 4
COPLAY_0=0;COPLAY_1=1;COPLAY_2=2;COPLAY_3=3     # multi-player code, four player only
COPLAYERLIST = [COPLAY_0, COPLAY_1, COPLAY_2, COPLAY_3]
BUFFER_SIZE = 80960
SERVER_ADDR = ("172.18.32.186", 4783)
CLIENT_ADDR = (socket.gethostname(), 4784)
HTTP_ADDR = ('172.18.32.186', 8888)
NET_DEFAULT_BACKLOG = 4
NET_DEFAULT_TIMEOUT = 10
NET_SERVER_NOTIFY_DIFF = 60 # nofity every diff frames

# encode and encode render info
EN_DO_CODE_RENDER_MASKS = (2**6-1, 2**4-1, 2**9-1, 2**1-1)
def encodeRenderInfo(img, rid, img_rt, fb):
    res = 0
    res += EN_DO_CODE_RENDER_MASKS[0] & img; res <<= 4
    res += EN_DO_CODE_RENDER_MASKS[1] & rid; res <<= 9
    res += EN_DO_CODE_RENDER_MASKS[2] & img_rt; res <<= 1
    res += EN_DO_CODE_RENDER_MASKS[3] & fb
    return res

def decodeRenderInfo(encode_data):
    fb = encode_data & EN_DO_CODE_RENDER_MASKS[3]; encode_data >>= 1
    img_rt = encode_data & EN_DO_CODE_RENDER_MASKS[2]; encode_data >>= 9
    rid = encode_data & EN_DO_CODE_RENDER_MASKS[1]; encode_data >>= 4
    img = encode_data & EN_DO_CODE_RENDER_MASKS[0]
    return (img, rid, img_rt, fb)

# init
pygame.init()
pygame.key.set_repeat(1, 10)
# Global Source
SCREEN = pygame.display.set_mode(SCREENWH, 0, 32)
IMAGES = []
FILENAME = ('img/player.png',
            'img/enemy.png',
            'img/wall.png',
            'img/gun.png',
            'img/bullet.png',
            'img/died.png')
for fn in FILENAME:
    try:
        img = pygame.image.load(fn).convert()
        img.set_colorkey(COLORKEY)
        IMAGES.append(img)
    except Exception, e:
        print(e, file=open('CoLog.txt', 'a'))
        print("Error, image %s failed to load" % (fn),
            file=open('CoLog.txt', 'a'))
        raw_input("Error Occurred!!! see log file for more...")
        pygame.quit()
        quit()
        
# Standard Vector
STD_NORTH_VECTOR = pygame.math.Vector2(0, 1)

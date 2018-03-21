# -*- coding: utf-8 -*-

import random

from kaiengine import settings
from kaiengine.display import createLabel, getWindowDimensionsScaled
from kaiengine.objectinterface import GraphicInterface, SchedulerInterface, EventInterface
from kaiengine.resource import toStringPath
from kaiengine.sDict import sDict
from kaiengine.audio import playMusic, playSound

from libraries.player import Player
from libraries.boulder import Boulder, BoulderSmall1, BoulderSmall2

from libraries.config import *


BOULDER_SPAWN_START_TIME = 120
BOULDER_SPAWN_BASE_RATE = 120
BOULDER_SPAWN_VARIANCE = .75
BOULDER_SPAWN_RATE_REDUCTION = .85
BOULDER_SPAWN_REDUCTION_APPLICATION_TIME = 180

BOULDER_OBJECTS = [Boulder, BoulderSmall1, BoulderSmall2]

HEART_Y_POS = 192
HEART_X_START_POS = 16
HEART_X_OFFSET = 24

HIGH_SCORE = "high_score"

GAME_RESTART_TIME = 180

glob = None


def initializeGamestate():
    global glob
    glob = Gamestate()
    
def closeGamestate():
    if glob:
        glob.destroy()
    
    
    
    
class Gamestate(SchedulerInterface, EventInterface):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player_health = 3
        self.boulder_spawn_rate = 1.0
        self.distance = 0.0
        
        self.background = GraphicInterface()
        self.background.setSprite(toStringPath(*BG_PATH))
        self.other_bg = GraphicInterface()
        self.other_bg.setSprite(toStringPath(*OTHER_BG_PATH))
        self.other_bg.setSpriteLayer(-1)
        
        self.player = None
        self.boulders = sDict()
        self.hearts = []
        for i in range(3):
            self.hearts.append(GraphicInterface())
            self.hearts[i].setSprite(toStringPath(*HEART_PATH))
            self.hearts[i].setPos(HEART_X_START_POS + HEART_X_OFFSET*i, HEART_Y_POS)
            self.hearts[i].setSpriteLayer(30)
        self.distance_counter = createLabel("", font = "kaimono3.gfont2")
        self.distance_counter.setPos(y = HEART_Y_POS)
        self.distance_counter.layer = 30
        
        self.max_distance_counter = createLabel("", font = "kaimono3.gfont2")
        self.max_distance_counter.setPos(y = HEART_Y_POS - 12)
        self.max_distance_counter.layer = 30
        
        playMusic(toStringPath(MUSIC_PATH))
        
        self.resetGame()
        
        self.Schedule(self.updateBGScroll, 1, True)
        self.Schedule(self.boulderSpawnReduction, BOULDER_SPAWN_REDUCTION_APPLICATION_TIME, True)
        self.Schedule(self.checkCollision, 1, True)
        self.Schedule(self.updateDistance, 1, True)
        
        self.addCustomListener(REMOVE_BOULDER_EVENT, self.removeBoulder)
        
    def resetGame(self):
        self.distance = 0.0
        self.player_health = 3
        self.boulder_spawn_rate = 1.0
        if self.player:
            self.player.destroy()
        self.player = Player()
        self.player.setPos(200,144)
        self.player.setSpriteAnimation("RUN")
        self.player.setSpriteLayer(10)
        for boulder in self.boulders.values():
            boulder.destroy()
        self.boulders.clear()
        self.updateHearts()
        self.Unschedule(self.spawnBoulder)
        self.Schedule(self.spawnBoulder, BOULDER_SPAWN_START_TIME)
        
    def spawnBoulder(self):
        self.boulders.append(random.choice(BOULDER_OBJECTS)())
        self.boulders.last_item().setIndex(self.boulders.last_key())
        
        current_rate = BOULDER_SPAWN_BASE_RATE*self.boulder_spawn_rate
        self.Schedule(self.spawnBoulder, int(current_rate*BOULDER_SPAWN_VARIANCE + (current_rate*(1.0-BOULDER_SPAWN_VARIANCE)*2*random.random())))
        
    def boulderSpawnReduction(self):
        self.boulder_spawn_rate *= BOULDER_SPAWN_RATE_REDUCTION
        
    def removeBoulder(self, index):
        try:
            self.boulders[index].destroy()
            del self.boulders[index]
        except KeyError:
            pass
        
    def updateBGScroll(self):
        if self.background:
            tex_dim = list(self.background.getSpriteTexDimensions())
            tex_dim[0] += BG_SCROLL_RATE
            tex_dim[1] += BG_SCROLL_RATE
            self.background.setSpriteTexDimensions(*tex_dim)
        if self.other_bg:
            tex_dim = list(self.other_bg.getSpriteTexDimensions())
            tex_dim[0] += BG_SCROLL_RATE/10
            tex_dim[1] += BG_SCROLL_RATE/10
            self.other_bg.setSpriteTexDimensions(*tex_dim)
            
    def checkCollision(self):
        if self.player and not self.player.checkInvulnerable() and not self.player.checkDead():
            for boulder in self.boulders.values():
                playerpos = self.player.getPos()
                boulderpos = boulder.getPos()
                if (playerpos[0] < boulderpos[0] + boulder.getSpriteWidth() and playerpos[0] + self.player.getSpriteWidth() > boulderpos[0]) and (playerpos[1] < boulderpos[1] + boulder.getSpriteHeight() and playerpos[1] + 16 > boulderpos[1]) and self.player.getZPos() <= boulder.getBoulderZHeight():
                    self.playerHit()
                    break
                    
    def playerHit(self):
        self.player_health -= 1
        self.updateHearts()
        self.player.gotHit()
        playSound(toStringPath(*HIT_SE_PATH))
        if self.player_health <= 0:
            self.player.setKilled()
            settings.setValue(HIGH_SCORE, max(settings.getValue(HIGH_SCORE, 0.0), self.distance))
            self.Schedule(self.resetGame, GAME_RESTART_TIME)
    
    def updateHearts(self):
        for i in range(3):
            if i < self.player_health:
                self.hearts[i].setSpriteAnimation("FULL")
            else:
                self.hearts[i].setSpriteAnimation("EMPTY")
                
    def updateDistance(self):
        if not self.player.checkDead():
            self.distance += 0.1
        self.distance_counter.setText("Distance: " + str(round(self.distance, 1)))
        self.distance_counter.setPos(x = getWindowDimensionsScaled()[0] - self.distance_counter.width - 16)
        self.max_distance_counter.setText("Max Distance: " + str(round(max(settings.getValue(HIGH_SCORE, 0.0), self.distance), 1)))
        self.max_distance_counter.setPos(x = getWindowDimensionsScaled()[0] - self.max_distance_counter.width - 16)
    
    def destroy(self):
        super().destroy()
        if self.background:
            self.background.destroy()
        if self.player:
            self.player.destroy()
        self.background = None
        self.player = None
        
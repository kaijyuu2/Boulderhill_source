# -*- coding: utf-8 -*-

from kaiengine.display import getWindowDimensionsScaled
from kaiengine.resource import toStringPath
from kaiengine.objectinterface import SchedulerInterface, GraphicInterface, EventInterface

from libraries.keyheld import checkKeyHeld

from libraries.config import *


PLAYER_MOVEMENT_SPEED_Y = 2
PLAYER_MOVEMENT_SPEED_X = 2.5

INVULNERABLE_TIME = 60

JUMP_STARTING_SPEED = 8
JUMP_GRAVITY = 0.4

class Player(SchedulerInterface, GraphicInterface, EventInterface):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jumping = False
        self.invulnerable = False
        self.z_pos = 0
        self.jump_speed = 0
        self.jumping_y_speed = 0
        self.jumping_x_speed = 0
        self.dead = False
        
        self.shadow = GraphicInterface()
        self.shadow.setSprite(toStringPath(*PLAYER_SHADOW_PATH))
        self.shadow.setSpriteCenter(True,True)
        self.shadow.setSpriteLayer(0.5)
        
        self.setSprite(toStringPath(*PLAYER_CHAR_PATH))
        
        self.Schedule(self.updateMovement, 1, True)
        
        self.addCustomListener(PLAYER_JUMP_EVENT, self.playerJump)
        
        
    def getZPos(self):
        return self.z_pos
        
    def updateMovement(self):
        self.z_pos += self.jump_speed
        if self.z_pos < 0:
            self.jumpFinished()
        pos = list(self.getPos())
        xspeed = 0
        yspeed = 0
        if not self.jumping:
            if not self.dead:
                if checkKeyHeld(MOVE_UP):
                    yspeed = PLAYER_MOVEMENT_SPEED_Y
                elif checkKeyHeld(MOVE_DOWN):
                    yspeed = -PLAYER_MOVEMENT_SPEED_Y
                if checkKeyHeld(MOVE_RIGHT):
                    xspeed = PLAYER_MOVEMENT_SPEED_X
                elif checkKeyHeld(MOVE_LEFT):
                    xspeed = -PLAYER_MOVEMENT_SPEED_X
        else:
            yspeed = self.jumping_y_speed
            xspeed = self.jumping_x_speed
        if not self.dead:
            pos[0] = max(0, min(getWindowDimensionsScaled()[0] - self.getSpriteWidth(), pos[0] + xspeed))
        pos[1] = max(0, min(MAX_Y_POSITION, pos[1] + yspeed))
        self.setPos(*pos)
        
    def playerJump(self):
        if not self.jumping and not self.invulnerable:
            self.jumping_y_speed = 0
            self.jumping_x_speed = 0
            if checkKeyHeld(MOVE_UP):
                self.jumping_y_speed = PLAYER_MOVEMENT_SPEED_Y
            elif checkKeyHeld(MOVE_DOWN):
                self.jumping_y_speed = -PLAYER_MOVEMENT_SPEED_Y
            if checkKeyHeld(MOVE_RIGHT):
                self.jumping_x_speed = PLAYER_MOVEMENT_SPEED_X
            elif checkKeyHeld(MOVE_LEFT):
                self.jumping_x_speed = -PLAYER_MOVEMENT_SPEED_X
            self.jumping = True
            self.setSpriteAnimation("JUMP")
            self.jump_speed = JUMP_STARTING_SPEED
            self.scheduleUnique(self.updateGravity, 1, True)
            
    def jumpFinished(self):
        self.z_pos = 0
        self.jump_speed = 0
        self.Unschedule(self.updateGravity)
        self.jumping = False
        if not self.invulnerable:
            self.setSpriteAnimation("RUN")
        
    def updateGravity(self):
        self.jump_speed -= JUMP_GRAVITY
        
    def checkInvulnerable(self):
        return self.invulnerable
    
    def gotHit(self):
        self.invulnerable = True
        self.setSpriteAnimation("HURT")
        self.Schedule(self.flashAnimation, 2, True)
        self.Schedule(self.finishInvulnerability, INVULNERABLE_TIME)
        
    def flashAnimation(self):
        self.setSpriteAlpha(abs(self.getSpriteAlpha() - 1.0))
        
    def finishInvulnerability(self):
        self.Unschedule(self.flashAnimation)
        self.setSpriteAlpha(1.0)
        if not self.dead:
            self.setSpriteAnimation("RUN")
        else:
            self.setSpriteAnimation("DEAD")
            self.Schedule(self.deathFallBehind, 1, True)
        self.invulnerable = False
        
    def setKilled(self):
        self.dead = True
        
    def checkDead(self):
        return self.dead
        
    def deathFallBehind(self):
        self.setPos(self.getPos()[0] - BG_SCROLL_RATE)
        
    #overwritten stuff
    
    
    def _updateSpritePos(self):
        pos = self.getPos()
        try: self.sprite.setPos(pos[0], pos[1] + self.z_pos)
        except AttributeError: pass
        self.shadow.setPos(pos[0] + self.getSpriteWidth()/2, pos[1] + 1)
        
        
    def destroy(self):
        super().destroy()
        if self.shadow:
            self.shadow.destroy()
        self.shadow = None
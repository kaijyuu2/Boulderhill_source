# -*- coding: utf-8 -*-

import random

from kaiengine.display import getWindowDimensionsScaled
from kaiengine.resource import toStringPath
from kaiengine.objectinterface import SchedulerInterface, GraphicInterface, MovementInterfaceFrames
from kaiengine.event import customEvent

from libraries.config import *

BOULDER_X_START_POS = -32
BOULDER_VELOCITY = 60

OFFSCREEN_BUFFER = 48

class _BoulderBase(MovementInterfaceFrames, GraphicInterface):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boulder_z_height = 16
        self.index = None
        
        self.setVelocity(x = BOULDER_VELOCITY)
        self.setPos(BOULDER_X_START_POS, random.random()*MAX_Y_POSITION)
        
        self.setSpriteLayer(1)
        
        self.Schedule(self.checkOffscreen, 60, True)
        
    def setIndex(self, index):
        self.index = index
        
        
    def checkOffscreen(self):
        if self.getPos()[0] > getWindowDimensionsScaled()[0] + OFFSCREEN_BUFFER:
            customEvent(REMOVE_BOULDER_EVENT, self.index)
            
    def getBoulderZHeight(self):
        return self.boulder_z_height
        
        
        

class Boulder(_BoulderBase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boulder_z_height = 24
        
        self.setSprite(toStringPath(BOULDER_PATH + ["boulder.png"]))
        
        
class BoulderSmall1(_BoulderBase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setSprite(toStringPath(BOULDER_PATH + ["bouldersmall1.png"]))
        
class BoulderSmall2(_BoulderBase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setSprite(toStringPath(BOULDER_PATH + ["bouldersmall2.png"]))
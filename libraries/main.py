# -*- coding: utf-8 -*-

from libraries.config import *

from kaiengine import settings
settings.initialize(DYNAMIC_SETTINGS_DEFAULTS) #can change in config's __init__
#done very early here to allow access to settings in initialization of imported modules

from kaiengine.fonts import initializeFonts
from kaiengine.logging import initLogger
from kaiengine import camera, event
from kaiengine.gameframehandler import  initializeGameFrames, closeGameFrames
from kaiengine.setup import *
from kaiengine.debug import debugMessage, checkDebugOn
from kaiengine.interfacekai import initializeBaseLayer

from libraries.interfacekai import ControlLayer
from libraries.gamestate import initializeGamestate

import os

#main game init
def init():
    initLogger()
    event.addGameCloseListener(close)

    if checkDebugOn():
        debugMessage("WARNING: Launching in debug mode")

    #setup main window and initialize drivers
    setupWindowBasic("logo.png")

    setupDrivers()
    initializeFonts()
    
    initializeBaseLayer(ControlLayer)
    initializeGamestate()

    initializeGameFrames(main_loop)

#main game loop
def main_loop(dt):
    pass




#game closed
def close():
    closeGameFrames()
    settings.saveToFile()
    closeDrivers()


# -*- coding: utf-8 -*-

from kaiengine.gconfig import *

from .local_keybinds import *
from .datakeys import *
from .paths import *
from .customevents import *



DYNAMIC_SETTINGS_DEFAULTS = {DYNAMIC_SETTINGS_GAME_CAPTION: "Boulder Hill", #overwrite defaults here
                    DYNAMIC_SETTINGS_KEY_BINDS: KEY_BINDS,
                    DYNAMIC_SETTINGS_GLOBAL_SCALING: 2,
                    DYNAMIC_SETTINGS_WINDOW_DIMENSIONS: [256, 224],
                    DYNAMIC_SETTINGS_FPS_ON: False}



DIRECTION_UP = 0 #enum for directions
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

BG_SCROLL_RATE = 2

MAX_Y_POSITION = 144
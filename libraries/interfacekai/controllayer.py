# -*- coding: utf-8 -*-

from kaiengine.interfacekai import InterfaceLayer
from kaiengine.keybinds import keyMatches
from kaiengine.event import callQuery, customEvent

from libraries.config import *


class ControlLayer(InterfaceLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    
    def respondKeyPress(self, symbol, modifiers):
        if keyMatches(CANCEL, symbol):
            customEvent(PLAYER_JUMP_EVENT)
        return False
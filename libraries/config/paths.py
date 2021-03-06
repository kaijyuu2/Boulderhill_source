# -*- coding: utf-8 -*-

from kaiengine.gconfig.paths import *


BG_FOLDER = "bgs"
CHAR_FOLDER = "char"
BOULDER_FOLDER = "boulders"
UI_FOLDER ="ui"

BG_PATH = [RESOURCE_PATH, GRAPHICS_PATH, BG_FOLDER, "background.png"]
OTHER_BG_PATH = [RESOURCE_PATH, GRAPHICS_PATH, BG_FOLDER, "title_screen.png"]
PLAYER_CHAR_PATH = [RESOURCE_PATH, GRAPHICS_PATH, CHAR_FOLDER, "char.png"]
PLAYER_SHADOW_PATH = [RESOURCE_PATH, GRAPHICS_PATH, CHAR_FOLDER, "playershadow.png"]
BOULDER_PATH = [RESOURCE_PATH, GRAPHICS_PATH, BOULDER_FOLDER]
HEART_PATH = [RESOURCE_PATH, GRAPHICS_PATH, UI_FOLDER, "heart.png"]
MUSIC_PATH = [RESOURCE_PATH, AUDIO_PATH, "music","music.ogg"]
HIT_SE_PATH = [RESOURCE_PATH, AUDIO_PATH, "fx","hit.ogg"]
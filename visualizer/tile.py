from enum import Enum
from ursina import *

class TileType(Enum):
    GROUND = 1
    AIR = 2
    START = 3
    END = 4

class Tile():
    def __init__(self,position, texture, type):
        self.position = position
        self.texture = texture
        self.type = type
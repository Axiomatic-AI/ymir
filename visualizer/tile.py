'''
Create a 'Tile' object with type and (x,y) location. 
'''
from enum import Enum
from ursina import *

class TileType(Enum):
    GROUND = 1
    AIR = 2
    START = 3
    END = 4
    START_TOP = 5
    END_TOP = 6
    WATER = 7

class Tile():
    def __init__(self, position, texture, type):
        self.position = position
        self.texture = texture
        self.type = type

    @property
    def x(self):
        return self.position[0]

    def __repr__(self):
        return str(self.type) + " at " + str(self.position)

    @property
    def y(self):
        return self.position[1]
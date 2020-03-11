import numpy as np
from visualizer.sprite.util import *
from abc import ABC, abstractmethod
from collections import defaultdict
from .animator import Animator
from .tile import Tile
from visualizer.constants import GRAVITY


class Sprite(Tile, ABC):
    def __init__(self, position, typ, controller, **kwargs):
        self.gravity = kwargs.pop("gravity", True)
        z_index = kwargs.pop("z_index", 5) # what 'layer' is the sprite rendered on
                                           # default level is 5
                                            # (larger means farther away from camera) 
                                            # pop so that you can't pass two z-indexes to __init__
        super().__init__(position, typ, controller, **kwargs, z_index=z_index)

        self.can_jump = True
        self.position = np.array(position, dtype = 'float64')
        self.velocity = np.array([0, 0], dtype='float64')
        self.friction = 0.1  # value between 0 and 1; larger means more friction
        self.horizontal_speed = 10.0
        self.jump_speed = 2.0
        self.on_moving_tile = False
        self.dead = False
        self.last_collided = None   # the list of Tiles which the sprite is currently colliding with?

    def update_render(self):
        self.entity.x = self.position[0]
        self.entity.y = self.position[1]
        self.entity.z = -1 # render on top of everything else

    def update_collisions(self, tiles, tile_array):
        collided = defaultdict(list)

        if len(tiles) == 0:
            pass

        if len(tiles) == 2:
            # vertically stacked tiles, snap horizontally
            t = tiles[0]
            if tiles[0].x == tiles[1].x:
                collided[collide(self, t, x=True, commit=True)].append(t)
            else: # horizontally connected tiles, snap vertically
                collided[collide(self, t, x=False, commit=True)].append(t)
        else:
            # position snapping, only if a single tile is collided, this will be buggy
            for tile in tiles:
                if self.velocity[0] != 0:
                    v = self.velocity[0]
                    if self.on_moving_tile:
                        v = self.on_moving_tile.speed * 10
                    horiz_time = min(abs(self.position[0] - tile.x - 1.0)
                                    , abs(self.position[0] + 1.0 - tile.x)) / abs(v)
                else:
                    horiz_time = 1000
                if self.velocity[1] != 0:
                    vert_time = min(abs(self.position[1] - tile.y - 1.0)
                                    , abs(self.position[1] + 1.0 - tile.y)) / abs(self.velocity[1])
                else:
                    vert_time = 1000

                # print(tile, vert_time, horiz_time, self.velocity)

                if vert_time == horiz_time:
                    collided[collide(self, tile, x=True, commit=False)].append(tile)
                    collided[collide(self, tile, x=False, commit=False)].append(tile)
                    collide(self, tile, x=True, commit=True)
                    collide(self, tile, x=False, commit=True)

                elif vert_time < horiz_time:
                    # vertical position snapping
                    collided[collide(self, tile, x=False, commit=False)].append(tile)
                    collide(self, tile, x=False, commit=True)
                else:
                    # horizontal position snapping
                    collided[collide(self, tile, x=True, commit=False)].append(tile)
                    collide(self, tile, x=True, commit=True)

        self.last_collided = collided
        return collided

    #abstract please overwrite me
    @abstractmethod
    def update(self, dt):
        self.update_position_velocity(dt)
        self.update_render()
        if self.animator:
            self.animator.update()

    def update_position_velocity(self, dt):
        self.on_moving_tile = False
        self.position += self.velocity * dt
        self.velocity[0] += -self.velocity[0] * (1-self.friction) * dt # slow down due to friction
        if self.gravity and not self.on_ground:
            self.velocity[1] += GRAVITY * dt

    def collide(self, tile, direction, commit=True):
        return False

    def die(self):
        self.controller.sprites.remove(self)
        self.dead = True

    @property
    def on_ground(self):
        down = self.last_collided.get(Direction.DOWN)
        return down and any(i.type.is_ground() for i in down)
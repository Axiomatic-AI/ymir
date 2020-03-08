'''
Central hub of the code, basically. Calls the necessary functions to 
render the scene, get input, move the player, etc. 
'''
from visualizer.player import Player
import numpy as np
from visualizer.FileReader import *
from ursina import *

scale = 1
dt = .1
camera_fov = 20
camera_offset = [0, 1, -30]
camera_speed = 2
gravity = -.5

h, w = window.size
OFFSET_X = 0
OFFSET_Y = 0
del h, w


class Controller():
    def __init__(self):
        self.app = Ursina()
        self.tile_array = []
        camera.orthographic = True
        camera.fov = camera_fov
        window.borderless = False
        self.moving_tiles = []
        self.sprites = []
        # window.fullscreen = True

    def update(self):
        for sprite in self.sprites:
            sprite.update_collisions(self.sprite_colliding(sprite), self.tile_array)
            sprite.update(dt)

        if self.player.position[1] < 0:
            self.die()

        add = len(self.moving_tiles) == 0

        for y, i in enumerate(self.tile_array):
            for x, j in enumerate(i):
                if add and isinstance(j, HorizontalMovingTile):
                    self.moving_tiles.append(j)
                j.update()

    def die(self):
        self.player.position = np.add(np.array(self.starting_tile.position, dtype='float64'), [0, 0])
        # todo: camera shift, slowdown, killcam?, say "crushed" or "shot" ala ROR1
        # todo: particle explosion animation
    # returns the ground tiles collided with, or an empty list for no collisions
    def sprite_colliding (self, sprite):
        ground_tiles = get_nearby_ground_tiles(sprite.position, self.tile_array, player=isinstance(sprite, Player))
        ground_tiles.extend(self.moving_tiles)
        collided_tiles = list(filter(lambda x: inside(sprite.position, x), ground_tiles))
        return collided_tiles

    def build_from_array(self, array):
        """Given a tile array, create the entities necessary for game rendering."""
        self.tile_array = array
        for y, row in enumerate(array):
            for x, tile in enumerate(row):
                if tile.texture is None: continue
                tile.controller = self
                tile.entity = Entity(model="quad",
                                     texture=tile.texture,
                                     scale=scale,
                                     position=(round(OFFSET_X + scale * tile.x),
                                               round(OFFSET_Y + scale * tile.y), 0))
                if tile.type == TileType.START:
                    self.starting_tile = tile
                elif tile.type == TileType.END:
                    self.ending_tile = tile

                tile.setup()

    def load_level(self, level_file_name):
        """Start a level from a file. Initialize player position, etc."""
        reader = FileReader(level_file_name)
        self.build_from_array(reader.read())
        self.player.position = np.add(np.array(self.starting_tile.position, dtype='float64'), [0, 2])

    def start(self):
        self.player = Player(position=np.array([0, 2], dtype='float64'),
                             entity=Entity(model="cube", color=color.blue, scale=1))
        camera.parent = self.player.entity
        camera.add_script(SmoothFollow(target=self.player.entity, offset=camera_offset, speed=camera_speed))
        input_handler.bind('right arrow', 'd')
        input_handler.bind('left arrow', 'a')
        input_handler.bind('up arrow', 'w')
        input_handler.bind('down arrow', 's')

        self.sprites.append(self.player)

        self.load_level("visualizer/test_file_2.txt")
        self.die() # to respawn player

        self.app.run()

    def unlock(self, typ):
        for row in self.tile_array:
            for t in row:
                if t.type.value == typ.value + 1:
                    t.hide()

    def tile_at(self, x, y):
        x, y = int(x), int(y)
        if 0 <= y < len(self.tile_array) and 0 <= x < len(self.tile_array[y]):
            return self.tile_array[y][x]

    def next_tile(self, tile, direction):
        if isinstance(direction, Direction):
            dx, dy = direction.diff
        else:
            dx, dy = direction

        l = len(self.tile_array)
        px, py = int(tile.position[0] + dx), l - (int(tile.position[1] + dy)) - 1

        return self.tile_at(px, py)

    def next_is_ground(self, tile, direction):
        n = self.next_tile(tile, direction)
        return n and n.type.is_ground()

    def next_ground(self, tile, direction):
        curr = list(map(int, tile.position))
        while True:
            t = self.tile_at(*curr)
            if not t or t.type.is_ground():
                break

            curr[0] += direction.dx
            curr[1] += direction.dy
        return [abs(tile.position[0] - curr[0]) - 1, abs(tile.position[1] - curr[1]) - 1]
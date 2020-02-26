import math
from visualizer import control
from visualizer.tile import TileType


def mag(a):
    return math.sqrt(sum([x * x for x in a]))


# Tells if an entity (anything with an ordered pair position vector) is inside the given tile
def inside(player, tile):
    density = 10
    for i in range(0, density):
        if point_inside([player.position[0] + control.scale * i / density, player.position[1]], tile):
            return True
        if point_inside([player.position[0] + control.scale * i / density, player.position[1] + control.scale],
                        tile):
            return True
        if point_inside([player.position[1], player.position[1] + control.scale * i / density], tile):
            return True
        if point_inside([player.position[1] + control.scale, player.position[1] + control.scale * i / density],
                        tile):
            return True
    return False


# tells if a position is inside a tile
def point_inside(point, tile):
    if tile.x <= point[0] <= tile.x + control.scale and tile.y <= point[1] <= tile.y + control.scale:
        return True
    return False


# gets tiles near a location (in a 2x2)
def get_nearby_ground_tiles(position, tile_array):
    position /= control.scale
    return list(filter(lambda x: x.type == TileType.GROUND, [tile_array[int(position[1])][int(position[0])],
                                                             tile_array[int(position[1]) + 1][int(position[0])]
        , tile_array[int(position[1])][int(position[0]) + 1], tile_array[int(position[1]) + 1][int(position[0]) + 1]]))

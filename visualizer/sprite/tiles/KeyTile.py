from visualizer.sprite.tile import Tile

class KeyTile(Tile):
    def collide(self, tile, direction):
        self.controller.unlock(self.type)
        self.hide(now=True)
        return False

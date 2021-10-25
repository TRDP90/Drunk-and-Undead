import pyasge
from tile import MapTile


# Changed values from 0, 16 on lines 11 and 9

class MapLayer:
    def __init__(self, layer: int, layermap):
        self.layer = layer
        self.tiles = []
        for i in range(0, 30):
            new = []
            for j in range(0, 25):
                new.append(MapTile())
            self.tiles.append(new)
        self.initTile(layermap)

# Changed values from 64 to 32 as art is 32bit

    def initTile(self, layermap) -> None:
        y_pos = 0
        for row in self.tiles:
            x_pos = 0
            for tile in row:
                tile.sprite.y = y_pos
                tile.sprite.x = x_pos
                tile.sprite.z_order = self.layer
                tile.sprite_number = layermap[int(y_pos / 32)][int(x_pos / 32)]
                x_pos = x_pos + 32
            y_pos = y_pos + 32

    def render(self, renderer: pyasge.Renderer) -> None:
        for row in self.tiles:
            for tile in row:
                if tile.sprite.texture:
                    renderer.render(tile.sprite)

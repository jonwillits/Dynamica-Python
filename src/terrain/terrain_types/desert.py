from src.terrain import terrain


class Desert(terrain.Tile):
    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Desert'
        self.image = 'assets/images/desert.gif'

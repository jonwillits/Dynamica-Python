from src.terrain import terrain


class Lake(terrain.Tile):
    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Lake'
        self.image = 'assets/images/lake.gif'

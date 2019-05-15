from src.terrain import terrain


class Plains(terrain.Tile):
    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Plains'
        self.image = 'assets/images/plains.gif'

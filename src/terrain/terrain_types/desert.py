from src.terrain import terrain
import numpy as np
from src import config


class Desert(terrain.Tile):
    class_appearance = np.random.randint(2, size=config.World.appearance_size)

    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Desert'
        self.image = 'assets/images/desert.gif'
        self.appearance = np.copy(Desert.class_appearance)
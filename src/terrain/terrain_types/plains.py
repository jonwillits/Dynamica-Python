from src.terrain import terrain
from src import config
import numpy as np


class Plains(terrain.Tile):
    class_appearance = np.random.randint(2, size=config.World.appearance_size)

    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Plains'
        self.image = 'assets/images/plains.gif'
        self.appearance = np.copy(Plains.class_appearance)

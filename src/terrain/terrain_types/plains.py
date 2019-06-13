from src.terrain import terrain
import numpy as np


class Plains(terrain.Tile):

    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Plains'
        self.image = 'assets/images/plains.gif'

        self.rgb = np.array([90., 160., 80.]) / 255
        self.appearance = np.concatenate((np.ones(10)*self.rgb[0], np.ones(10)*self.rgb[1], np.ones(10)*self.rgb[2]))
        self.appearance += np.random.uniform(-0.02, 0.02, size=30)



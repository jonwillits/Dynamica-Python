from src.terrain import terrain
import numpy as np


class Ocean(terrain.Tile):

    def __init__(self, x, y):
        terrain.Tile.__init__(self, x, y)
        self.terrain_type = 'Ocean'
        self.image = 'assets/images/ocean.gif'

        self.rgb = np.array([15., 90., 210.]) / 255
        self.appearance = np.concatenate((np.ones(10)*self.rgb[0], np.ones(10)*self.rgb[1], np.ones(10)*self.rgb[2]))
        self.appearance += np.random.uniform(-0.02, 0.02, size=30)

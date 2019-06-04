from src import config
from src.plants import plants
import numpy as np


class Grass(plants.Plant):

    ############################################################################################################
    def __init__(self, id_number, the_world, position, tile_fertility):
        plants.Plant.__init__(self, id_number, the_world, position, tile_fertility)
        self.species = 'Grass'
        self.grow_rate = config.Grass.grow_rate

        self.rgb = np.array([90., 160., 80.]) / 255
        self.appearance = np.concatenate((np.ones(10)*self.rgb[0], np.ones(10)*self.rgb[1], np.ones(10)*self.rgb[2]))
        self.appearance += np.random.uniform(-0.02, 0.02, size=30)

    ############################################################################################################
    def next_turn(self):
        self.quantity += self.grow_rate * self.tile_fertility
        if self.quantity > (100 * self.tile_fertility):
            self.quantity = 100 * self.tile_fertility

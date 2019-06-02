from src import config
from src.plants import plants
import numpy as np


class Grass(plants.Plant):
    class_appearance = np.random.randint(2, size=config.World.appearance_size)

    ############################################################################################################
    def __init__(self, id_number, the_world, position, tile_fertility):
        plants.Plant.__init__(self, id_number, the_world, position, tile_fertility)
        self.species = 'Grass'
        self.appearance = np.copy(Grass.class_appearance)
        self.grow_rate = config.Grass.grow_rate

    ############################################################################################################
    def next_turn(self):
        self.quantity += self.grow_rate * self.tile_fertility
        if self.quantity > (100 * self.tile_fertility):
            self.quantity = 100 * self.tile_fertility

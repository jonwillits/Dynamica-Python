from src import config
from src.plants import plants
import numpy as np


class Grass(plants.Plant):
    ############################################################################################################
    def __init__(self, id_number):
        plants.Plant.__init__(self, id_number)
        self.species = 'Grass'
        self.appearance = np.random.randint(0, 2, config.World.appearance_size)
        self.appearance[0] = self.quantity/100
        self.grow_rate = config.Grass.grow_rate

    ############################################################################################################
    def next_turn(self):
        self.quantity += self.grow_rate
        if self.quantity > 100:
            self.quantity = 100
        self.appearance[0] = self.quantity/100

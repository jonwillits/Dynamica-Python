from src import config
import random


############################################################################################################
############################################################################################################
class Plant:
    ############################################################################################################
    def __init__(self, id_number, the_world, position, tile_fertility):
        self.the_world = the_world
        self.kingdom = "Plant"
        self.position = position
        self.graphic_object = None
        self.species = None
        self.id_number = id_number
        self.quantity = None
        self.appearance = None
        self.age = 0
        self.tile_fertility = tile_fertility

    ############################################################################################################
    def __repr__(self):
        output_string = self.species + " #" + str(self.id_number) + " Quantity: " + str(self.quantity)
        return output_string

    ############################################################################################################
    def init_plant(self):

        self.quantity = 100 * self.tile_fertility

        for i in range(config.World.appearance_size):
            if random.random() < config.Plant.appearance_variance:
                if self.appearance[i] == 0:
                    self.appearance[i] = 1
                else:
                    self.appearance[i] = 0

        self.appearance[0] = self.quantity / 100

    ############################################################################################################
    def next_turn(self):
        self.age += 1
        self.appearance[0] = self.quantity / 100


############################################################################################################
############################################################################################################


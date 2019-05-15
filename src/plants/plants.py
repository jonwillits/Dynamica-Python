from src import config
import numpy as np
import random


############################################################################################################
############################################################################################################
class Plant:
    ############################################################################################################
    def __init__(self, the_world):
        self.the_world = the_world
        self.kingdom = "Plant"
        self.position = [None, None]
        self.graphic_object = None
        self.image = None
        self.species = None
        self.id_number = self.the_world.entity_counter
        self.the_world.entity_counter += 1
        self.quantity = 100
        self.appearance = None
        self.age = 0

    ############################################################################################################
    def __repr__(self):
        output_string = self.species + " #" + str(self.id_number) + " Quantity: " + str(self.quantity)
        return output_string

    ############################################################################################################
    def change_appearance(self, appearance):
        self.appearance = appearance
        for i in range(len(self.appearance)):
            choice = random.random()
            if choice < config.Plant.appearance_variance:
                if self.appearance[i] == 0:
                    self.appearance[i] = 1
                else:
                    self.appearance[i] = 0

    ############################################################################################################
    def next_turn(self):
        self.age += 1


############################################################################################################
############################################################################################################


from src import config
import random


class Tile:
    ############################################################################################################
    def __init__(self, x, y):

        self.animal_list = []
        self.plant_list = []
        self.object_list = []
        self.tile_x = x
        self.tile_y = y
        self.graphic_object = None
        self.terrain_type = None
        self.image = None
        self.appearance = None

    ############################################################################################################
    def __repr__(self):
        output_string = "{} - Animals: {}".format(self.terrain_type, len(self.animal_list))
        return output_string

    ############################################################################################################
    def change_appearance(self, appearance):
        self.appearance = appearance

        for i in range(len(self.appearance)):
            choice = random.random()
            if choice < config.Terrain.appearance_variance:
                if self.appearance[i] == 0:
                    self.appearance[i] = 1
                else:
                    self.appearance[i] = 0



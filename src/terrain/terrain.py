from src import config


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
        self.fertility = None

    ############################################################################################################
    def __repr__(self):
        output_string = "{} - Animals: {}".format(self.terrain_type, len(self.animal_list))
        return output_string

    def init_terrain(self):
        self.fertility = config.Terrain.fertility_dict[self.terrain_type]

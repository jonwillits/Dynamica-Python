import random
import numpy as np


############################################################################################################
############################################################################################################
class WorldObject:
    ############################################################################################################
    def __init__(self):
        self.position = [None, None]
        self.object_type = None
        self.graphic_object = None
        self.image = None
        self.appearance = None
        self.quantity = None

    ############################################################################################################
    def next_turn(self):
        pass


############################################################################################################
############################################################################################################
class Carcass(WorldObject):
    ############################################################################################################
    def __init__(self, object_type, image, appearance, appearance_diff, size=1):
        WorldObject.__init__(self)
        self.object_type = object_type
        self.image = image
        self.quantity = 100 * size
        self.appearance = appearance

        self.init_appearance(appearance_diff)

    ############################################################################################################
    def init_appearance(self, appearance_diff):
        for i in range(len(self.appearance)):
            choice = random.random(0, 1)
            if choice < appearance_diff:
                if self.appearance[i] == 0:
                    self.appearance[i] = 1
                else:
                    self.appearance[i] = 0

    ############################################################################################################
    def next_turn(self):
        self.quantity -= 5



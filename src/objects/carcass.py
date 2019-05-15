from src.objects import world_object
from src import config


class Carcass(world_object.WorldObject):
    ############################################################################################################
    def __init__(self, kind, image, appearance, size, the_world):
        world_object.WorldObject.__init__(self)
        self.kind = kind
        self.quantity = 100 * size
        self.appearance = appearance
        self.the_world = the_world
        self.init_appearance()
        self.id_number = the_world.entity_counter
        self.graphic_object = image
        self.decay_rate = config.Carcass.decay_rate

        self.the_world.entity_counter += 1

    ############################################################################################################
    def init_appearance(self):
        if len(self.appearance) < 10:
            num_dead_bits = 3
        else:
            num_dead_bits = 5

        for i in range(num_dead_bits):
            self.appearance[-i] = 0.5

    ############################################################################################################
    def next_turn(self):
        self.quantity -= self.decay_rate
        if self.quantity <= 0:
            self.the_world.map[tuple(self.position)].object_list.remove(self)
            self.the_world.object_counts_dict[self.kind] -= 1
            self.the_world.object_list.remove(self)
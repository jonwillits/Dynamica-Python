from src.animals import animals
from src import config


class Lion(animals.Animal):
    def __init__(self, animal_id, mother_genome, father_genome):
        animals.Animal.__init__(self, animal_id, mother_genome, father_genome)
        self.species = 'Lion'
        self.image_dict = {0: 'assets/images/Lion0.gif', 90: 'assets/images/Lion90.gif',
                           180: 'assets/images/Lion180.gif', 270: 'assets/images/Lion270.gif'}
        self.dead_graphic_object = 'assets/images/dead_lion.gif'
        self.diet_dict = config.Lion.diet_dict
        self.species_metabolism_multiplier = config.Lion.species_metabolism_multiplier
        self.metabolism = config.Animal.metabolism * self.species_metabolism_multiplier

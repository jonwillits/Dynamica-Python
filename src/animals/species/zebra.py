from src.animals import animals
from src import config


class Zebra(animals.Animal):
    def __init__(self, animal_id, mother_genome, father_genome):
        animals.Animal.__init__(self, animal_id, mother_genome, father_genome)
        self.species = 'Zebra'
        self.image_dict = {0: 'assets/images/Zebra0.gif', 90: 'assets/images/Zebra90.gif',
                           180: 'assets/images/Zebra180.gif', 270: 'assets/images/Zebra270.gif'}
        self.dead_graphic_object = 'assets/images/dead_zebra.gif'
        self.diet_dict = config.Zebra.diet_dict
        self.species_metabolism_multiplier = config.Zebra.species_metabolism_multiplier
        self.metabolism = config.Animal.metabolism * self.species_metabolism_multiplier

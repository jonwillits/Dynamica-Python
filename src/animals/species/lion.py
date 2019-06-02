from src.animals import animals


class Lion(animals.Animal):

    def __init__(self, animal_id, mother_genome, father_genome):
        animals.Animal.__init__(self, animal_id, mother_genome, father_genome)

        self.species = 'Lion'
        self.trait_init_dict = Lion.trait_init_dict

        self.image_dict = {0: 'assets/images/Lion0.gif',
                           90: 'assets/images/Lion90.gif',
                           180: 'assets/images/Lion180.gif',
                           270: 'assets/images/Lion270.gif'}

        self.dead_graphic_object = 'assets/images/dead_lion.gif'

        self.allowed_terrain_dict = {'Plains': True,
                                     'Desert': True,
                                     'Lake': False,
                                     'Ocean': False}

    allowed_start_terrain = ['Plains', 'Desert']

    # see below for explanation
    trait_init_dict = {'Sex': (0, 'int', None, 'immutable', 'invisible'),
                       'Max Size': (1, 'int', None, 'mutable', 'invisible'),
                       'Digest Plants': (2, 'float', (0.0, 0.0), 'mutable', 'invisible'),
                       'Digest Meat': (2, 'float', (1.0, 0.0), 'mutable', 'invisible'),
                       'Sharp Teeth': (2, 'float', (1.0, 0.0), 'mutable', 'visible'),

                       'Num Hidden Neurons': (3, 'int', None, 'mutable', 'invisible'),
                       'Weight Init Stdev': (3, 'float', None, 'mutable', 'invisible'),
                       'Prediction Learning Rate': (4, 'float', None, 'mutable', 'invisible'),
                       'Health Value Target': (2, 'float', (1.0, 0.0), 'immutable', 'invisible'),
                       'Energy Value Target': (2, 'float', (1.0, 0.0), 'immutable', 'invisible'),
                       'Arousal Value Target': (2, 'float', (0.0, 0.0), 'immutable', 'invisible'),

                       'Health Learning Rate': (4, 'float', None, 'mutable', 'invisible'),
                       'HealthD Learning Rate': (4, 'float', None, 'mutable', 'invisible'),
                       'Energy Learning Rate': (4, 'float', None, 'mutable', 'invisible'),
                       'EnergyD Learning Rate': (4, 'float', None, 'mutable', 'invisible'),
                       'Arousal Learning Rate': (4, 'float', None, 'mutable', 'invisible'),
                       'ArousalD Learning Rate': (4, 'float', None, 'mutable', 'invisible'),

                       'Rest Bias': (1, 'int', None, 'mutable', 'invisible'),
                       'Attack Bias': (1, 'int', None, 'mutable', 'invisible'),
                       'Eat Bias': (1, 'int', None, 'mutable', 'invisible'),
                       'Procreate Bias': (1, 'int', None, 'mutable', 'invisible'),
                       'Turn Bias': (1, 'int', None, 'mutable', 'invisible'),
                       'Move Bias': (1, 'int', None, 'mutable', 'invisible'),
                       'Arousal Growth': (1, 'int', None, 'mutable', 'invisible'),
                       'Action Noise': (2, 'float', (.01, .00), 'mutable', 'invisible'),

                       'Fur': (2, 'float', (1.0, 0.05), 'mutable', 'visible'),
                       'Scales': (2, 'float', (0.0, 0.0), 'mutable', 'visible'),
                       'Feathers': (2, 'float', (0.0, 0.0), 'mutable', 'visible'),

                       'Stripes': (2, 'float', (0.0, 0.05), 'mutable', 'visible'),
                       'Spots': (2, 'float', (0.0, 0.05), 'mutable', 'visible'),

                       'Primary Coloring R': (2, 'float', (0.80, 0.02), 'mutable', 'visible'),
                       'Primary Coloring G': (2, 'float', (0.60, 0.02), 'mutable', 'visible'),
                       'Primary Coloring B': (2, 'float', (0.35, 0.02), 'mutable', 'visible'),
                       'Secondary Coloring R': (2, 'float', (0.30, 0.02), 'mutable', 'visible'),
                       'Secondary Coloring G': (2, 'float', (0.20, 0.02), 'mutable', 'visible'),
                       'Secondary Coloring B': (2, 'float', (0.15, 0.02), 'mutable', 'visible')
                       }

    # this specifies the genetic makeup and phenotype of a species
    # each labeled gene has three associated values
    #   1) the size of the gene
    #   2) the type of gene it is, which affects how the gene's binary sequence is translated into a phenotype value
    #       the choices being
    #       - int: the binary vector is converted to an integer between 1 and 10^n, where n is the gene size
    #       - float: the binary vector is converted into a decimal between 0 and 1, where the gradations are in sizes
    #           of 1/10^n, where n is the gene size. So if gene size = 2, that means values can be 0.01, 0.02, ... 1.00
    #           uf gene size = 3, values can be 0.001, 0.002, ... 1.000
    #       - vector: the binary vector is copied, with the resulting phenotype value itself being a binary vector
    #   3) what the initial population mean and standard deviation should be (mean, stdev).
    #           If set, each animal will be assigned a value drawn from a population with those parameters
    #           If None, random value within legal range will be selected
    #   4) whether mutation on this trait is allowed
    #       note that if trait values are initially set to be random, or with variance in the initial population,
    #       evolution from recombination may still occur
    #       trait will only be truly immutable if no variance exists in the initial population, AND set to immutable
    #   5) whether the trait is visible, ie whether it becomes a feature in the animal's appearance vector
    #       note that regardless, animal's appearance vector will contain features showing:
    #       - current size
    #       - age
    #       - pregnancy status
    #       - northward facing status
    #       - eastward facing status
    #       - current health level
    #       - current energy level
    #       - current arousal level



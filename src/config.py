############################################################################################################
class World:
    random_seed = None
    world_rows = 3  # rows x grid size-1 must be < window_height
    world_columns = 3  # columns x grid size-1 must be < window_width
    appearance_variance = 0.05  # the probability each feature of an object's appearance varies from its prototype


############################################################################################################
class Terrain:
    plains_prob = .5  # then each grid tile has this chance of being made into plains
    lake_prob = .0  # then each grid tile has this chance of being made into lake
    fertility_dict = {'Plains': 1.00,      # the amount of plants (grass) that can exist in each terrain type,
                      'Desert': 0.05,      # and also how quickly it grows back if eaten
                      'Lake': 0.00,        # multiplying this number by the plant species's grow rate
                      'Ocean': 0.00}


############################################################################################################
class Animal:

    teeth_attack_strength = (1, 20)  # attack strength for 100% flat teeth to 100% sharp teeth

    plant_energy = 1                # amount of energy derived from eating 1 unit of plant
    meat_energy = 10                # amount of energy derived from eating 1 unit of  meat

    pregnancy_chance = 1.0          # probability of pregnancy given reproductive act
    mutation_rate = 0.01            # probability of mutation on any given gene
    gestation_rate = 50             # number of turns to produce a child
    childhood_length = 100          # number of turns of childhood

    metabolism = 2.0                    # general multiplier for energy cost of all actions
    pregnant_metabolism_multiplier = 2  # increased energy cost for actions while pregnant
    starvation_rate = 1.0               # health lost each turn energy = 0

    # effects of each action on energy, health, and arousal
    # note that other effects exist but defined elsewhere
    # the effect of eating on energy is this value, plus the energy gained from the eating act itself,
    #   which is defined in terms of what nad how much is eaten, and the organism's genetic ability to digest the food,
    #   which is a function of tooth type and digestion type
    #   effect of procreation on arousal is it's own gene
    action_drive_change_dict = {'Rest':      {'Health': 1.0, 'Energy': -0.01, 'Arousal': 0.0},
                                'Attack':    {'Health': 0.0, 'Energy': -0.10, 'Arousal': 0.0},
                                'Eat':       {'Health': 0.0, 'Energy': -0.03, 'Arousal': 0.0},
                                'Procreate': {'Health': 0.0, 'Energy': -0.05, 'Arousal': 0.0},
                                'Turn':      {'Health': 0.1, 'Energy': -0.02, 'Arousal': 0.0},
                                'Move':      {'Health': 0.0, 'Energy': -0.10, 'Arousal': 0.0}}

    pop_size = {'Lion': 2,
                'Zebra': 2}


############################################################################################################
class Plant:
    grow_rate = 5


############################################################################################################
class WorldObject:
    decay_rate = 5

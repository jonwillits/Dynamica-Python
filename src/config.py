############################################################################################################
class GlobalOptions:
    debug = False
    random_seed = None
    summary_freq = 1        # how often animal summary info is printed to the terminal window
    timing_freq = 0         # how often timing summary info is printed to the screen (mostly for analyzing performance)
    window_height = 800
    window_width = 1600


############################################################################################################
class World:
    num_rows = 30  # rows x grid size-1 must be < window_height
    num_columns = 30  # columns x grid size-1 must be < window_width


############################################################################################################
class Terrain:
    plains_prob = .5  # then each grid tile has this chance of being made into plains
    lake_prob = .1  # then each grid tile has this chance of being made into lake
    appearance_variance = 0.05  # the probability each feature of a terrain tile's appearance varies from its prototype

    # the amount of plants (grass) that can exist in each terrain type, and also how quickly it grows back if eaten,
    #    multiplying this number by the plant species's grow rate
    fertility_dict = {'Plains': 1.00,
                      'Desert': 0.05,
                      'Lake': 0.00,
                      'Ocean': 0.00}


############################################################################################################
class Plant:
    appearance_variance = 0.05  # the probability each feature of a plant's appearance varies from its prototype


############################################################################################################
class WorldObject:
    appearance_variance = 0.05  # the probability each feature of an object's appearance varies from its prototype


############################################################################################################
class Animal:
    output_data = False

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

    # initial start values of the three drives
    drive_init_dict = {'Health': 1.0, 'Energy': 1.0, 'Arousal': 0.0}

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


############################################################################################################
class Lion:
    start_number = 20


############################################################################################################
class Zebra:
    start_number = 30


############################################################################################################
class Grass:
    grow_rate = 5


############################################################################################################
class Carcass:
    decay_rate = 1


############################################################################################################
class Debug:
    drive_system = False
    action_system = False
    nervous_system = False

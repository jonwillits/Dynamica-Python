from src import config
from src.terrain.terrain_types import lake, plains, desert, ocean
from src.animals.species import lion, zebra
from src.plants.species import grass
from src.objects import carcass
import random
import time
import sys
import numpy as np


class World:
    def __init__(self):

        self.current_turn = 0
        self.entity_counter = 0

        self.world_size = 0
        self.land_size = 0
        self.water_size = 0
        self.num_rows = config.World.num_rows + 2
        self.num_columns = config.World.num_columns + 2
        self.map = {}

        self.animal_list = []
        self.plant_list = []
        self.object_list = []
        self.dead_animal_list = []
        self.plant_species_counts_dict = {}
        self.animal_species_counts_dict = {}
        self.object_counts_dict = {}

        self.turn_summary_dict = None
        self.initial_animal_summary_dict = None

        self.appearance_dict = None
        random_seed = config.GlobalOptions.random_seed
        if random_seed is None:
            self.random_seed = random.randint(0, 32768)
        else:
            self.random_seed = config.GlobalOptions.random_seed

        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

        self.generate_world()
        self.generate_plants()
        self.generate_animals()
        self.generate_objects()
        self.calc_turn_summary()
        self.calc_initial_animal_summaries()

        self.world_timers_array = np.zeros([12])

        # if config.Animal.output_data:
        #     self.animal_summary_filename = "output/" + str(self.random_seed) + "_animals_n" + str(len(self.animal_list)) + ".txt"

    ############################################################################################################
    def generate_world(self):
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                self.world_size += 1
                new_tile = self.choose_tile_type(i, j)
                self.map[(j, i)] = new_tile
        self.land_size = self.world_size - self.water_size

    ############################################################################################################
    def choose_tile_type(self, i, j):
        if (i == 0) or (i == self.num_rows - 1) or (j == 0) or (j == self.num_columns - 1):
            new_tile = ocean.Ocean(j, i)
            new_tile.init_terrain()
            self.water_size += 1
        else:
            lake_value = random.uniform(0, 1)
            if lake_value < config.Terrain.lake_prob:
                new_tile = lake.Lake(j, i)
                new_tile.init_terrain()
                self.water_size += 1
            else:
                plains_value = random.uniform(0, 1)
                if plains_value < config.Terrain.plains_prob:
                    new_tile = plains.Plains(j, i)
                    new_tile.init_terrain()
                else:
                    new_tile = desert.Desert(j, i)
                    new_tile.init_terrain()

        return new_tile

    ############################################################################################################
    def generate_plants(self):

        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if self.map[(j, i)].fertility > 0:
                    new_grass = grass.Grass(self.entity_counter, self, (j, i), self.map[(j, i)].fertility)
                    self.entity_counter += 1
                    new_grass.init_plant()
                    self.map[(j, i)].plant_list.append(new_grass)
                    self.plant_list.append(new_grass)

                    if 'Grass' not in self.plant_species_counts_dict:
                        self.plant_species_counts_dict['Grass'] = 1
                    else:
                        self.plant_species_counts_dict['Grass'] += 1

    ############################################################################################################
    def generate_animals(self):

        for i in range(config.Lion.start_number):
            new_animal = lion.Lion(self, None, None)
            new_animal.init_animal()
            self.animal_list.append(new_animal)

        for i in range(config.Zebra.start_number):
            new_animal = zebra.Zebra(self, None, None)
            new_animal.init_animal()
            self.animal_list.append(new_animal)

        if len(self.animal_list) > self.land_size:
            print("ERROR: Number of animals is > the number of land tiles")
            sys.exit(2)
        else:
            random.shuffle(self.animal_list)

            for i in range(len(self.animal_list)):

                if self.animal_list[i].species not in self.animal_species_counts_dict:
                    self.animal_species_counts_dict[self.animal_list[i].species] = 1
                else:
                    self.animal_species_counts_dict[self.animal_list[i].species] += 1

                self.place_animal(self.animal_list[i])
                self.animal_list[i].nervous_system.update_sensory_state()

    ############################################################################################################
    def place_animal(self, animal, position=None):
        if position is None:
            placed = False
            while not placed:
                column = random.randint(1, self.num_columns - 2)
                row = random.randint(1, self.num_rows - 2)
                current_tile = self.map[(column, row)]
                terrain_type = current_tile.terrain_type
                if animal.allowed_terrain_dict[terrain_type]:
                    if len(self.map[(column, row)].animal_list) == 0:
                        placed = True
                        animal.position = [column, row]
                        self.map[(column, row)].animal_list.append(animal)
        else:
            animal.position = [position[0], position[1]]
            self.map[(position[0], position[1])].animal_list.append(animal)

    ############################################################################################################
    def generate_objects(self):
        # entity_counter += 1
        pass

    ############################################################################################################
    def calc_turn_summary(self):
        self.turn_summary_dict = {'Plant': {}, 'Animal': {}, 'Object': {}}

        for species in self.plant_species_counts_dict:
            self.turn_summary_dict['Plant'][species] = [self.plant_species_counts_dict[species], 0]
            for plant in self.plant_list:
                self.turn_summary_dict['Plant'][plant.species][1] += plant.quantity

        for species in self.animal_species_counts_dict:
            self.turn_summary_dict['Animal'][species] = [self.animal_species_counts_dict[species], 0, 0, 0]

        for animal in self.animal_list:
            self.turn_summary_dict['Animal'][animal.species][1] += animal.drive_system.drive_value_array[0]
            self.turn_summary_dict['Animal'][animal.species][2] += animal.drive_system.drive_value_array[1]
            self.turn_summary_dict['Animal'][animal.species][3] += animal.drive_system.drive_value_array[2]

        for species in self.animal_species_counts_dict:
            if self.turn_summary_dict['Animal'][species][0]:
                self.turn_summary_dict['Animal'][species][1] /= self.turn_summary_dict['Animal'][species][0]
                self.turn_summary_dict['Animal'][species][2] /= self.turn_summary_dict['Animal'][species][0]
                self.turn_summary_dict['Animal'][species][3] /= self.turn_summary_dict['Animal'][species][0]

    ############################################################################################################
    def calc_initial_animal_summaries(self):
        self.initial_animal_summary_dict = {}
        for species in self.animal_species_counts_dict:
            animal_summary_dict = self.calc_species_summary(species)
            self.initial_animal_summary_dict[species] = animal_summary_dict

    ############################################################################################################
    def calc_species_summary(self, species):

        animal_summary_dict = {'N': self.turn_summary_dict['Animal'][species][0],
                               'Drive Values': self.turn_summary_dict['Animal'][species][1:]}
        sex_sum = 0.0
        age_sum = 0.0
        size_sum = 0.0
        hidden_sum = 0.0
        learning_rate_sum = 0.0
        weight_init_stdev_sum = 0.0
        drive_target_sums = np.zeros([3], float)
        drive_reinforcement_sums = np.zeros([2, 3], float)
        action_output_sums = np.zeros([6], float)

        for animal in self.animal_list:
            if animal.species == species:
                input_state, hidden_state, output_state = animal.nervous_system.neural_feedforward()
                sensory_outputs = output_state[animal.nervous_system.s_indexes[0]:animal.nervous_system.s_indexes[1] + 1]
                drive_outputs = output_state[animal.nervous_system.d_indexes[0]:animal.nervous_system.d_indexes[1] + 1]
                action_outputs = output_state[animal.nervous_system.a_indexes[0]:animal.nervous_system.a_indexes[1] + 1]
                action_argument_outputs = output_state[animal.nervous_system.aa_indexes[0]:animal.nervous_system.aa_indexes[1] + 1]

                if animal.phenotype.trait_value_dict['Sex'] == 1:
                    sex_sum += 1
                age_sum += animal.age
                size_sum += animal.phenotype.trait_value_dict['Max Size']
                hidden_sum += animal.phenotype.trait_value_dict['Num Hidden Neurons']
                learning_rate_sum += animal.phenotype.trait_value_dict['Prediction Learning Rate']
                weight_init_stdev_sum += animal.phenotype.trait_value_dict['Weight Init Stdev']
                drive_target_sums += animal.nervous_system.drive_target_array
                drive_reinforcement_sums += animal.nervous_system.drive_reinforcement_rate_matrix
                action_output_sums += action_outputs

        if animal_summary_dict['N'] > 0:
            n = animal_summary_dict['N']
        else:
            n = 1

        animal_summary_dict['Sex'] = sex_sum / n
        animal_summary_dict['Age'] = age_sum / n
        animal_summary_dict['Size'] = size_sum / n
        animal_summary_dict['Hidden Neurons'] = hidden_sum / n
        animal_summary_dict['Prediction Learning Rate'] = learning_rate_sum / n
        animal_summary_dict['Weight Init Stdev'] = weight_init_stdev_sum / n
        animal_summary_dict['Drive Targets'] = drive_target_sums / n
        animal_summary_dict['Drive Reinforcement Rates'] = drive_reinforcement_sums / n
        animal_summary_dict['Action Outputs'] = action_output_sums / n

        return animal_summary_dict

    ############################################################################################################
    def next_turn(self):

        # take a turn for each nonliving object in the world
        start_time = time.time()
        if len(self.object_list):
            for world_object in self.object_list:
                world_object.next_turn()
        self.world_timers_array[0] += time.time() - start_time

        # take a turn for each plant in the world
        start_time = time.time()
        if len(self.plant_list):
            for plant in self.plant_list:
                plant.next_turn()
        self.world_timers_array[1] += time.time() - start_time

        # take a turn for each animal in the world
        if len(self.animal_list):
            for animal in self.animal_list:
                # normal turn actions
                animal.take_turn()

                # deal with pregnancy related matters
                start_time = time.time()
                if animal.pregnant:
                    if animal.pregnant == 1:

                        if animal.species == 'Zebra':
                            animal.fetus = zebra.Zebra(self, animal.genome, animal.baby_daddy_genome)
                        elif animal.species == 'Lion':
                            animal.fetus = lion.Lion(self, animal.genome, animal.baby_daddy_genome)
                        animal.fetus.init_animal()

                    if animal.pregnant >= config.Animal.gestation_rate:

                        x = animal.position[0]
                        y = animal.position[1]

                        location_list = [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
                        random.shuffle(location_list)

                        for location in location_list:
                            if self.legal_offspring_location(animal, location):
                                self.animal_list.append(animal.fetus)
                                self.place_animal(animal.fetus, location)
                                self.animal_species_counts_dict[animal.species] += 1
                                animal.bear_child()
                                break
                    else:
                        animal.pregnant += 1
                self.world_timers_array[9] += time.time() - start_time

                # deal with animal whose health is 0
                start_time = time.time()
                if animal.drive_system.drive_value_array[animal.drive_system.drive_index_dict['Health']] <= 0:
                    self.create_carcass(animal)
                    self.kill_animal(animal)
                self.world_timers_array[10] += time.time() - start_time

        # calculate turn summary information
        start_time = time.time()
        self.calc_turn_summary()
        self.world_timers_array[11] += time.time() - start_time

        # output turn summary information
        if config.GlobalOptions.summary_freq:
            if self.current_turn % config.GlobalOptions.summary_freq == 0:
                self.print_summary()
                if config.Animal.output_data:
                    self.write_summary()

        self.current_turn += 1

    ############################################################################################################
    def print_summary(self):

        output_header = "{:<5s} {:<14s}".format("Turn", "ID")
        output_header += "{:<9s} {:<7s} {:<5s}".format("Sex", "Age", "Size")
        output_header += " {:>3s},{:<3s} {:>4s} | ".format("X", "Y", "Dir")
        output_header += " {:<7s}  {:<7s}  {:<7s} | ".format("Health", "Energy", "Arousal")
        output_header += " {:<6s}  {:<6s} {:<6s} {:<6s} {:<6s} {:<6s}".format("Rest", "Attack", "Eat", "Proc", "Turn", "Move")
        output_header += "{:>9s}".format("Choice")
        output_header += "| {:>6s} {:>6s} {:>6s} {:>6s} {:>9s}".format("SpCost", "DpCost", "ApCost", "PpCost", "DrCost")
        if len(self.animal_list) > 1 or self.current_turn % 10 == 0:
            print(output_header)

        if len(self.animal_list) == 0:
            print("All Animals are Dead!")
        else:
            for animal in self.animal_list:

                output_string = "{:<5s} {:<14s}".format(str(self.current_turn), animal.species+"-"+str(animal.id_number))

                sex = str(animal.phenotype.trait_value_dict['Sex'])
                if animal.pregnant:
                    sex = sex + "+{}".format(animal.pregnant)
                output_string += "{:<9s} {:<7s} {:<5s}".format(sex, str(animal.age),
                                                               str('{:<1.3f}'.format(animal.current_size)))
                output_string += " {:>3s},{:<3s} {:>4s} |".format(str(animal.position[0]), str(animal.position[1]),
                                                                  str(animal.orientation))
                for i in range(animal.drive_system.num_drives):
                    trimmed_drive = "{:<5.3f}".format(animal.drive_system.drive_value_array[i])
                    output_string += "  {:>7s}".format(str(trimmed_drive))
                output_string += " | "

                for i in range(animal.action_system.num_actions):
                    try:
                        output_string += "  {:<3.2f} ".format(animal.action_system.legal_action_prob_distribution[i])
                    except ValueError as argument:
                        print('\n\n')
                        print(animal)
                        print(animal.genome)
                        print(animal.phenotype)
                        print(animal.drive_system)
                        print(animal.action_system)
                        print(animal.nervous_system)
                        print('\n' + str(argument) + '\n')
                        sys.exit(2)

                output_string += "{:>9s}".format(animal.action_system.action_choice)
                output_string += " | "
                spv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.s_indexes[0]:animal.nervous_system.s_indexes[1]]
                dpv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.d_indexes[0]:animal.nervous_system.d_indexes[1]]
                apv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.a_indexes[0]:animal.nervous_system.a_indexes[1]]
                aapv = animal.nervous_system.neural_network_prediction_cost[animal.nervous_system.aa_indexes[0]:animal.nervous_system.aa_indexes[1]]

                sp_error = np.absolute(spv).sum() / animal.nervous_system.s_size
                dp_error = np.absolute(dpv).sum() / animal.nervous_system.d_size
                ap_error = np.absolute(apv).sum() / animal.nervous_system.a_size
                aap_error = np.absolute(aapv).sum() / animal.nervous_system.aa_size

                output_string += '{:>6s} '.format('{:<3.2f}'.format(sp_error))
                output_string += '{:>6s} '.format('{:<3.2f}'.format(dp_error))
                output_string += '{:>6s} '.format('{:<3.2f}'.format(ap_error))
                output_string += '{:>6s} '.format('{:<3.2f}'.format(aap_error))

                print(output_string)

    ############################################################################################################
    def write_summary(self):
        pass

    ############################################################################################################
    def kill_animal(self, animal):
        self.dead_animal_list.append(animal)

        self.map[tuple(animal.position)].animal_list.remove(animal)
        self.animal_list.remove(animal)
        self.animal_species_counts_dict[animal.species] -= 1
        animal.position = None

    ############################################################################################################
    def create_carcass(self, animal):
        object_type = "Meat"
        animal_carcass = carcass.Carcass(object_type, animal.dead_graphic_object,
                                              animal.appearance, animal.current_size, self)
        animal_carcass.position = animal.position

        self.object_list.append(animal_carcass)
        self.map[tuple(animal_carcass.position)].object_list.append(animal_carcass)
        if object_type in self.object_counts_dict:
            self.object_counts_dict[object_type] += 1
        else:
            self.object_counts_dict[object_type] = 1

    ############################################################################################################
    def legal_offspring_location(self, animal, location):
        if animal.allowed_terrain_dict[self.map[location].terrain_type]:
            if len(self.map[location].animal_list) == 0:
                return True
            else:
                return False
        else:
            return False

import random
import numpy as np
from src import config
from src import nervous_system
np.set_printoptions(precision=5, suppress=True)


class Animal:

    def __init__(self, the_world, mother_genome, father_genome):

        ############################################################################################################
        self.the_world = the_world  # a reference to the world data structure
        self.kingdom = "Animal"  # this animal's kingdom type (ie plant or animal)
        self.species = None  # this animal's species type
        self.graphic_object = None  # this animal's graphic object, currently a python turtle object
        self.id_number = the_world.entity_counter  # a unique id number
        the_world.entity_counter += 1

        ############################################################################################################
        self.age = 0
        self.current_size = 0.1  # the animal's current size, global range 0-5, actual range specified genetically
        self.attack_strength = config.Animal.attack_strength  # the force modifier this animal gets when attacking
        self.diet_dict = None   # a dictionary specifying what this animal can eat, choices currently plants and/or meat

        ############################################################################################################
        self.position = None    # the animal's coordinates
        self.orientation = random.choice([0, 90, 180, 270])  # can make this nonrandom later
        self.allowed_terrain_dict = {'Desert': False,  # specific species make these true eventually this will go
                                     'Lake': False,    # away completely and be replaced by a 'can breathe in' feature,
                                     'Plains': False,  # where being out of breath will be painful and the animal will
                                     'Forest': False}  # learn to strongly dislike places it cannot breathe

        ############################################################################################################
        self.genome_size = None
        self.genome = None
        # genome is created below, and consists of a set of base pairs equal to the sum of:
        #   - the values in trait_gene_size_dict
        #   - the values in drive_state_gene_size_dict
        #   - the length of the appearance array

        ############################################################################################################
        self.num_traits = None
        self.trait_list = None
        self.trait_index_dict = None
        self.trait_value_dict = None
        self.trait_gene_location_dict = None
        self.trait_gene_size_sum = None
        self.trait_gene_size_dict = {'Sex': 1,
                                     'Max Size': 5,
                                     'Num Hidden Neurons': 8,
                                     'Learning Rate': 8}
        # each trait has it's own defining function below, translating the genes to a value

        ############################################################################################################
        self.drive_state_gene_size_dict = {'Health': (5, 5),
                                           'Energy': (5, 5),
                                           'Arousal': (5, 5)}
        self.drive_reinforcement_direction_dict = {'Health': 1, 'Energy': 1, 'Arousal': -1}
        self.num_drives = None
        self.drive_list = None
        self.drive_index_dict = None
        self.drive_gene_location_dict = None
        self.drive_gene_size_sum = None
        self.drive_reinforcement_direction_matrix = None

        self.drive_value_array = None
        self.last_drive_value_array = None
        self.drive_value_change_array = None
        self.metabolism = config.Animal.metabolism

        # each drive has two values that correspond to learning rates for positive and negative reinforcement learning
        # rates. in other words, given an increase in health health, how

        ############################################################################################################
        self.appearance = None
        self.appearance_size = None
        self.appearance_gene_locations = None

        ############################################################################################################
        self.num_actions = None  # the total number of actions available
        self.action_list = None  # the list of actions available
        self.action_index_dict = None  # an index dict for all actions

        self.action_neuron_number_dict = {'Rest': 1,
                                          'Attack': 1,
                                          'Eat': 1,
                                          'Procreate': 1,
                                          'Turn': 2,
                                          'Move': 2}
        self.num_action_neurons = None  # the number of action neurons total
        self.action_neuron_list = None  # a list of labels for the action neurons
        self.action_neuron_index_dict = None  # an index dict for each action to each neuron

        self.action_outputs = None  # the activity of all action units in the neural network output layer

        self.action_choice_array = None  # the activity of only action choice units, not action modifier units
        self.scaled_action_choice_array = None  # activity of action choice units scaled nonnegative and at least 0.01
        self.legal_action_array = None  # a binary array stating which actions are legal on the current turn
        self.gated_action_activations = None  # previous 2 multiplied together, zeroing out activity of illegal actions
        self.legal_action_prob_distribution = None  # previous turned into a prob distribution

        self.action_choice = None  # the action string that is chosen on the current turn
        self.action_choice_array = None  # a one-hot binary array showing the action taken this turn
        self.last_action_outputs = None  # an array showing the output activations on the previous turn
        self.last_action_choice = None  # the action string chosen on the previous turn
        self.last_action_array = None  # a one-hot array showing the action taken last turn

        self.patient_outputs = None  # the activation of the patient output neurons
        self.current_patient = None  # the array of the actually selected patient
        self.last_patient_outputs = None  # the activation of the patient from last turn
        self.last_patient_array = None  # the array of the last actually selected patient

        self.action_drive_change_dict = config.Animal.action_drive_change_dict
        self.action_history_list = None

        ############################################################################################################
        self.neural_network = None

        self.learning_rate = None

        self.view_list = None
        self.sensory_matrix = None
        self.tile_rep_size = None

        self.s_size = None
        self.d_size = None
        self.a_size = None
        self.p_size = None
        self.h_size = None
        self.input_size = None
        self.output_size = None

        self.s_indexes = None
        self.d_indexes = None
        self.a_indexes = None
        self.p_indexes = None

        self.neural_input = None
        self.neural_hidden_state = None
        self.neural_output = None
        self.last_neural_input = None
        self.last_neural_hidden_state = None
        self.last_neural_output = None
        self.neural_network_prediction_cost = None
        self.neural_network_drive_cost = None
        self.total_cost = None

        ############################################################################################################
        self.pregnant = 0
        self.fetus = None

        ############################################################################################################
        self.init_genome(mother_genome, father_genome)
        self.init_traits()
        self.init_drives()
        self.init_appearance()
        self.init_actions()
        self.init_neural_network()

    ############################################################################################################
    def __repr__(self):
        output_string = "{} {}\n".format(self.species, self.id_number)

        output_string += "    Age: {}\n".format(self.age)
        output_string += "    Size: {}\n".format(self.current_size)
        output_string += "    Position: {},{}\n".format(self.position[0], self.position[1])
        output_string += "    Orientation: {}\n".format(self.orientation)

        output_string += "    Genome Size: {}\n" \
                         "    Genome: {}\n".format(self.genome_size, ''.join(self.genome))

        output_string += "    Traits:\n"
        for trait in self.trait_value_dict:
            if isinstance(self.trait_value_dict[trait], float):
                output_string += "        {}: {:.4f}\n".format(trait, self.trait_value_dict[trait])
            else:
                output_string += "        {}: {}\n".format(trait, self.trait_value_dict[trait])

        output_string += "    Appearance: "
        for item in self.appearance:
            output_string += str(item)
        output_string += "\n"

        output_string += "    Drives:\n"
        for i in range(self.num_drives):
            output_string += "        {}: {:.1f}\n".format(self.drive_list[i], self.drive_value_array[i])

        output_string += "    Actions\n"
        for action_neuron in self.action_neuron_index_dict:
            output_string += "        {}: {}\n".format(action_neuron, self.action_neuron_index_dict[action_neuron])

        output_string += "    Neural Network:\n"
        output_string += "        Input Layer: {}\n".format(self.input_size)
        output_string += "            Sensory Size: {}\n".format(self.s_size)
        output_string += "            Drive Size: {}\n".format(self.d_size)
        output_string += "            Action Size: {}\n".format(self.a_size)
        output_string += "            Patient Size: {}\n".format(self.p_size)
        output_string += "        Hidden Layer: {}\n".format(self.h_size)
        output_string += "        Output Layer: {}\n".format(self.output_size)
        output_string += "            Sensory Size: {}\n".format(self.s_size)
        output_string += "            Drive Size: {}\n".format(self.d_size)
        output_string += "            Action Size: {}\n".format(self.a_size)
        output_string += "            Patient Size: {}\n".format(self.p_size)
        return output_string

    ############################################################################################################
    def init_genome(self, mother_genome, father_genome):
        """ if there are parents, then randomly choose a gene from the father or mother, with a
        chance of a mutation specified in the config file. if there are no parents, a genome is determined randomly"""
        self.genome = []

        if mother_genome:
            self.genome_size = len(mother_genome)
            for i in range(self.genome_size):
                child_pair = random.choice([mother_genome[i], father_genome[i]])
                if random.uniform(0, 1) < config.Animal.mutation_rate:
                    if child_pair == "GT" or child_pair == "TG":
                        child_pair = random.choice(["AC", "CA"])
                    elif child_pair == "AC" or child_pair == "CA":
                        child_pair = random.choice(["TG", "GT"])
                self.genome.append(child_pair)
        else:
            self.genome_size = 0
            for trait in self.trait_gene_size_dict:
                self.genome_size += self.trait_gene_size_dict[trait]
            for drive in self.drive_state_gene_size_dict:
                neg = self.drive_state_gene_size_dict[drive][0]
                pos = self.drive_state_gene_size_dict[drive][1]
                self.genome_size += (neg + pos)
            self.genome_size += config.World.appearance_size

            for i in range(self.genome_size):
                self.genome.append(random.choice(["AC", "CA", "GT", "TG"]))

    ############################################################################################################
    def init_traits(self):
        self.num_traits = 0
        self.trait_list = []
        self.trait_index_dict = {}
        self.trait_gene_location_dict = {}
        self.trait_gene_size_sum = 0
        self.trait_value_dict = {}
        for trait in self.trait_gene_size_dict:
            self.trait_list.append(trait)
            self.trait_index_dict[trait] = self.num_traits
            self.num_traits += 1
            gene_size = self.trait_gene_size_dict[trait]
            self.trait_gene_location_dict[trait] = (self.trait_gene_size_sum, self.trait_gene_size_sum + gene_size - 1)
            self.trait_gene_size_sum += gene_size

        self.trait_value_dict['Sex'] = self.determine_sex()
        self.trait_value_dict['Max Size'] = self.determine_size()
        self.trait_value_dict['Num Hidden Neurons'] = self.determine_num_hidden_units()
        self.trait_value_dict['Learning Rate'] = self.determine_learning_rate()

    ############################################################################################################
    def init_drives(self):

        self.num_drives = 0
        self.drive_list = []
        self.drive_gene_size_sum = self.trait_gene_size_sum
        self.drive_index_dict = {}
        self.drive_gene_location_dict = {}
        self.drive_reinforcement_direction_matrix = np.zeros([len(self.drive_state_gene_size_dict)], float)

        for drive in self.drive_state_gene_size_dict:
            self.drive_list.append(drive)
            self.drive_index_dict[drive] = self.num_drives
            self.drive_reinforcement_direction_matrix[self.num_drives] = self.drive_reinforcement_direction_dict[drive]
            self.num_drives += 1

            pos_gene_size = self.drive_state_gene_size_dict[drive][0]
            neg_gene_size = self.drive_state_gene_size_dict[drive][1]

            self.drive_gene_location_dict[drive] = (self.drive_gene_size_sum,
                                                    self.drive_gene_size_sum + pos_gene_size - 1,
                                                    self.drive_gene_size_sum + pos_gene_size,
                                                    self.drive_gene_size_sum + pos_gene_size + neg_gene_size - 1)
            self.drive_gene_size_sum = self.drive_gene_size_sum + pos_gene_size + neg_gene_size

        self.drive_value_array = np.ones([self.num_drives], float) * 100
        self.trait_value_dict['Drive Reinforcement Rates'] = self.determine_drive_reinforcement()

    ############################################################################################################
    def determine_sex(self):
        if self.genome[self.trait_gene_location_dict['Sex'][0]] == 'AC' or \
                self.genome[self.trait_gene_location_dict['Sex'][0]] == 'CA':
            return 'Female'
        else:
            return 'Male'

    ############################################################################################################
    def determine_size(self):
        start_gene = self.trait_gene_location_dict['Max Size'][0]
        stop_gene = self.trait_gene_location_dict['Max Size'][1]
        size_genes = self.genome[start_gene:stop_gene+1]
        size = 1
        for gene in size_genes:
            if gene == 'GT' or gene == 'TG':
                size += 1
        return size

    ############################################################################################################
    def determine_num_hidden_units(self):
        start_gene = self.trait_gene_location_dict['Num Hidden Neurons'][0]
        stop_gene = self.trait_gene_location_dict['Num Hidden Neurons'][1]
        num_hidden_genes = self.genome[start_gene:stop_gene+1]
        binary_string = ""
        for i in range(len(num_hidden_genes)):
            if num_hidden_genes[i] == "AC" or num_hidden_genes[i] == "CA":
                binary_string += "0"
            else:
                binary_string += "1"
        num_hidden_units = int(binary_string, 2)
        return num_hidden_units

    ############################################################################################################
    def determine_learning_rate(self):
        start_gene = self.trait_gene_location_dict['Learning Rate'][0]
        stop_gene = self.trait_gene_location_dict['Learning Rate'][1]
        learning_rate_genes = self.genome[start_gene:stop_gene+1]
        binary_string = ""
        for i in range(len(learning_rate_genes)):
            if learning_rate_genes[i] == "AC" or learning_rate_genes[i] == "CA":
                binary_string += "0"
            else:
                binary_string += "1"
        learning_rate = 1 / (int(binary_string, 2) + 1)
        return np.round(learning_rate, 4)

    ############################################################################################################
    def determine_drive_reinforcement(self):
        drive_reinforcement_matrix = np.zeros([2, self.num_drives], float)

        for i in range(self.num_drives):
            g1_start = self.drive_gene_location_dict[self.drive_list[i]][0]
            g1_end = self.drive_gene_location_dict[self.drive_list[i]][1]
            g2_start = self.drive_gene_location_dict[self.drive_list[i]][2]
            g2_end = self.drive_gene_location_dict[self.drive_list[i]][3]
            g1 = self.genome[g1_start:g1_end + 1]
            g2 = self.genome[g2_start:g2_end + 1]
            binary_string1 = ""
            binary_string2 = ""
            for j in range(len(g1)):
                if g1[j] == "AC" or g1[j] == "CA":
                    binary_string1 += "0"
                else:
                    binary_string1 += "1"
                if g2[j] == "AC" or g2[j] == "CA":
                    binary_string2 += "0"
                else:
                    binary_string2 += "1"
            learning_rate1 = 1 / (int(binary_string1, 2) + 1)
            learning_rate2 = 1 / (int(binary_string2, 2) + 1)
            drive_reinforcement_matrix[0, i] = np.round(learning_rate1, 5)
            drive_reinforcement_matrix[1, i] = np.round(learning_rate2, 5)

        return drive_reinforcement_matrix

    ############################################################################################################
    def init_appearance(self):
        # appearance[0] is always size, and starts 0. will change each turn as animal approaches 'Max Size'
        self.appearance_size = config.World.appearance_size
        self.appearance = np.zeros([self.appearance_size], int)
        self.appearance_gene_locations = (self.genome_size-self.appearance_size, self.genome_size-1)

        appearance_genes = self.genome[:self.appearance_size]
        for i in range(self.appearance_size):
            if appearance_genes[i] == 'AC' or appearance_genes[i] == 'CA':
                self.appearance[i] = 0
            else:
                self.appearance[i] = 1
        self.appearance[0] = self.current_size / 5

    ############################################################################################################
    def change_appearance(self, appearance):
        self.appearance = appearance
        gene_location = self.genome_size - config.World.appearance_size
        for i in range(len(self.appearance)):
            if random.random() < config.Animal.within_sex_variance:
                if self.appearance[i] == 0:
                    self.appearance[i] = 1
                else:
                    self.appearance[i] = 0
            if self.appearance[i] == 0:
                self.genome[gene_location + i] = random.choice(["AC", "CA"])
            else:
                self.genome[gene_location + i] = random.choice(["GT", "TG"])
        self.appearance[0] = self.current_size / 5

    ############################################################################################################
    def init_actions(self):

        self.num_actions = 0
        self.action_list = []
        self.action_index_dict = {}

        self.num_action_neurons = 0
        self.action_neuron_list = []
        self.action_neuron_index_dict = {}

        current = 0
        for action in self.action_neuron_number_dict:
            self.action_list.append(action)
            self.action_index_dict[action] = self.num_actions
            self.num_action_neurons += self.action_neuron_number_dict[action]
            self.action_neuron_index_dict[action] = current
            current += self.action_neuron_number_dict[action]
            self.action_neuron_list.append(action)
            if self.action_neuron_number_dict[action] > 1:
                for i in range(self.action_neuron_number_dict[action]-1):
                    self.action_neuron_list.append(None)
            self.num_actions += 1

    ############################################################################################################
    def init_neural_network(self):
        self.s_size = 5 * 4 * config.World.appearance_size
        self.d_size = self.num_drives
        self.a_size = self.num_action_neurons
        self.p_size = config.World.appearance_size
        self.h_size = self.trait_value_dict['Num Hidden Neurons']

        self.learning_rate = self.trait_value_dict['Learning Rate']

        self.s_indexes = (0, self.s_size-1)
        self.d_indexes = (self.s_size, self.s_size + self.d_size - 1)
        self.a_indexes = (self.s_size + self.d_size, self.s_size + self.d_size + self.a_size - 1)
        self.p_indexes = (self.s_size + self.d_size + self.a_size,
                          self.s_size + self.d_size + self.a_size + self.p_size - 1)

        self.input_size = self.s_size + self.d_size + self.a_size + self.p_size + self.h_size
        self.output_size = self.s_size + self.d_size + self.a_size + self.p_size

        self.neural_network = nervous_system.NeuralNetwork(self.input_size, self.h_size, self.output_size,
                                                           self.learning_rate, config.Animal.weight_init)
        self.tile_rep_size = 4 * config.World.appearance_size
        self.last_neural_hidden_state = np.random.randn(self.h_size)
        self.last_action_array = np.zeros(self.a_size)
        self.last_patient_array = np.zeros(self.p_size)
        self.last_patient_outputs = np.zeros(self.p_size)

    ############################################################################################################
    def take_turn(self):
        self.last_drive_value_array = np.copy(self.drive_value_array)

        self.get_sensory_representation()

        self.neural_feedforward(self.sensory_matrix, self.drive_value_array, self.last_action_array,
                                self.last_patient_array, self.last_neural_hidden_state)

        self.get_legal_action_probabilities()
        self.choose_action()
        self.choose_patient()
        self.take_action()
        self.update_drives()

        self.last_neural_input = self.neural_input
        self.last_neural_output = self.neural_output
        self.last_action_choice = self.action_choice
        self.last_action_outputs = self.action_outputs
        self.last_action_array = np.zeros(self.num_action_neurons)
        self.last_action_array[self.action_neuron_index_dict[self.action_choice]] = 1
        self.last_patient_outputs = self.patient_outputs
        self.last_patient_array = self.current_patient
        self.last_neural_hidden_state = self.neural_hidden_state

        self.update_neural_weights()

        self.grow_older()

    ############################################################################################################
    def get_sensory_representation(self):
        self.get_view_list()

        rep_list = []
        for view in self.view_list:
            rep_list.append(self.get_tile_representation(view))

        self.sensory_matrix = np.array(rep_list)

    ############################################################################################################
    def get_view_list(self):
        x = self.position[0]
        y = self.position[1]

        if self.orientation == 0:
            self.view_list = [(x, y), (x+1, y+1), (x+1, y), (x+1, y-1), (x+2, y)]
        elif self.orientation == 90:
            self.view_list = [(x, y), (x+1, y-1), (x, y-1), (x-1, y-1), (x, y-2)]
        elif self.orientation == 180:
            self.view_list = [(x, y), (x-1, y-1), (x-1, y), (x-1, y+1), (x-2, y)]
        elif self.orientation == 270:
            self.view_list = [(x, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x, y+2)]

    ############################################################################################################
    def get_tile_representation(self, tile_location):

        tile_representation_list = []
        x = tile_location[0]
        y = tile_location[1]

        if (x >= 0) and (y >= 0) and (x <= config.World.columns-1) and (y <= config.World.rows-1):
            tile_representation_list.append(self.the_world.map[x, y].appearance)
            if len(self.the_world.map[x, y].animal_list):
                tile_representation_list.append(self.the_world.map[x, y].animal_list[0].appearance)
            else:
                tile_representation_list.append(self.the_world.map[x, y].appearance)

            if len(self.the_world.map[x, y].plant_list):
                tile_representation_list.append(self.the_world.map[x, y].plant_list[0].appearance)
            else:
                tile_representation_list.append(self.the_world.map[x, y].appearance)

            if len(self.the_world.map[x, y].object_list):
                tile_representation_list.append(self.the_world.map[x, y].object_list[0].appearance)
            else:
                tile_representation_list.append(self.the_world.map[x, y].appearance)
        else:
            tile_representation_list.append(np.ones([config.World.appearance_size])*0.5)
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)

        tile_rep_array = np.array(tile_representation_list)

        return tile_rep_array

    ############################################################################################################
    def neural_feedforward(self, sensory_matrix, drive_value_array, last_action_array, last_patient_array,
                           last_hidden_state):

        sensory_array = sensory_matrix.flatten()
        scaled_drive_value_array = drive_value_array/50 - 1

        self.neural_input = np.concatenate((sensory_array, scaled_drive_value_array, last_action_array,
                                            last_patient_array, last_hidden_state))

        self.neural_hidden_state, self.neural_output = self.neural_network.feedforward(self.neural_input)

    ############################################################################################################
    def get_legal_action_probabilities(self):
        self.action_outputs = self.neural_output[self.a_indexes[0]:self.a_indexes[1] + 1]
        self.action_choice_array = np.zeros([self.num_actions], float)
        for i in range(self.num_actions):
            self.action_choice_array[i] = self.action_outputs[self.action_neuron_index_dict[self.action_list[i]]]
        self.scaled_action_choice_array = self.action_choice_array + abs(self.action_choice_array.min()) + .01
        self.legal_action_array = self.get_legal_action_array()
        self.gated_action_activations = self.scaled_action_choice_array * self.legal_action_array
        self.legal_action_prob_distribution = self.gated_action_activations / self.gated_action_activations.sum()

    ############################################################################################################
    def get_legal_action_array(self):

        legal_action_array = np.zeros([self.num_actions])

        # Resting and turning are always legal
        legal_action_array[self.action_index_dict['Rest']] = 1
        legal_action_array[self.action_index_dict['Turn']] = 1

        # if forward tile not allowable for species type, make move illegal
        if self.allowed_terrain_dict[self.the_world.map[self.view_list[2]].terrain_type]:
            legal_action_array[self.action_index_dict['Move']] = 1

        if len(self.the_world.map[self.view_list[2]].animal_list):
            legal_action_array[self.action_index_dict['Attack']] = 1
            legal_action_array[self.action_index_dict['Procreate']] = 1
            legal_action_array[self.action_index_dict['Move']] = 0

        # if not plant or object in current tile, make eat illegal
        if "Plants" in self.diet_dict:
            if len(self.the_world.map[self.view_list[0]].plant_list):
                legal_action_array[self.action_index_dict['Eat']] = 1

        if "Meat" in self.diet_dict:
            if len(self.the_world.map[self.view_list[0]].object_list):
                if self.the_world.map[self.view_list[0]].object_list.object_type == "Meat":
                    legal_action_array[self.action_neuron_index_dict['Eat']] = 1

        return legal_action_array

    ############################################################################################################
    def choose_action(self):
        action_choice_cumulative_probabilities = []
        cumulative_probability_sum = 0
        action_choice = None
        action_choice_number = random.random()
        for i in range(self.num_action_neurons):
            if self.legal_action_prob_distribution[i]:
                cumulative_probability_sum += self.legal_action_prob_distribution[i]
                action_choice_cumulative_probabilities.append(cumulative_probability_sum)
                if action_choice_number < cumulative_probability_sum:
                    action_choice = self.action_list[i]
                    break
        self.action_choice = action_choice

    ############################################################################################################
    def choose_patient(self):

        self.patient_outputs = self.neural_output[self.p_indexes[0]:self.p_indexes[1] + 1]

        patient_list = []
        patient = -1
        patient_sim = -1
        patient_array = None

        patient_norm = np.linalg.norm(self.patient_outputs)
        own_tile = self.view_list[0]
        forward_tile = self.view_list[2]

        counter = 0

        for plant in self.the_world.map[own_tile].plant_list:
            cos_sim = np.dot(plant.appearance, self.patient_outputs) / (np.linalg.norm(plant.appearance) * patient_norm)
            patient_list.append((self.position, "plant", plant.species, plant.id_number, cos_sim, plant.appearance))
            if cos_sim > patient_sim:
                patient = counter
                patient_sim = cos_sim
                patient_array = plant.appearance
            counter += 1

        for world_object in self.the_world.map[own_tile].object_list:
            cos_sim = np.dot(world_object.appearance, self.patient_outputs) / \
                      (np.linalg.norm(world_object.appearance) * patient_norm)
            patient_list.append((self.position, "world object", world_object.object_type,
                                 world_object.id_number, cos_sim, world_object.appearance))
            if cos_sim > patient_sim:
                patient = counter
                patient_sim = cos_sim
                patient_array = world_object.appearance
            counter += 1

        for animal in self.the_world.map[forward_tile].animal_list:
            cos_sim = np.dot(animal.appearance,
                             self.patient_outputs) / (np.linalg.norm(animal.appearance) * patient_norm)
            patient_list.append((self.position, "plant", animal.species, animal.id_number, cos_sim, animal.appearance))
            if cos_sim > patient_sim:
                patient = counter
                patient_sim = cos_sim
                patient_array = animal.appearance
            counter += 1

        if patient != -1:
            self.current_patient = patient_array
        else:
            self.current_patient = np.zeros([self.p_size], float)

    ############################################################################################################
    def take_action(self):
        if self.action_choice == 'Rest':
            self.rest()
        elif self.action_choice == 'Move':
            self.move()
        elif self.action_choice == 'Turn':
            self.turn()
        elif self.action_choice == 'Attack':
            self.attack()
        elif self.action_choice == 'Eat':
            self.eat()
        elif self.action_choice == 'Procreate':
            self.procreate()

    ############################################################################################################
    def rest(self):
        pass

    ############################################################################################################
    def move(self):

        x = self.position[0]
        y = self.position[1]

        new_x = x
        new_y = y
        if self.orientation == 0:
            new_x = x + 1
        elif self.orientation == 90:
            new_y = y - 1
        elif self.orientation == 180:
            new_x = x - 1
        elif self.orientation == 270:
            new_y = y + 1

        self.position = [new_x, new_y]
        self.the_world.map[(x, y)].animal_list.remove(self)
        self.the_world.map[(new_x, new_y)].animal_list.append(self)

    ############################################################################################################
    def turn(self):
        turn_amount = self.action_outputs[self.action_neuron_index_dict['Turn'] + 1]
        if 0.167 <= turn_amount <= 0.5:
            self.orientation += 270

        elif 0.5 <= turn_amount <= 0.833:
            self.orientation += 90

        elif turn_amount < 0.167 or turn_amount > 0.833:
            self.orientation += 180

        if self.orientation >= 360:
            self.orientation -= 360

    ############################################################################################################
    def attack(self):
        patient = self.the_world.map[(self.view_list[2])].animal_list[0]
        patient.drive_value_array[patient.drive_index_dict['Health']] -= self.attack_strength * self.current_size
        self.drive_value_array[patient.drive_index_dict['Health']] -= patient.attack_strength * \
            patient.current_size

    ############################################################################################################
    def eat(self):
        patient = None
        if "Meat" in self.diet_dict:
            if len(self.the_world.map[(self.view_list[0])].object_list):
                patient = self.the_world.map[(self.view_list[0])].object_list[0]
        if "Plants" in self.diet_dict:
            if len(self.the_world.map[(self.view_list[0])].plant_list):
                patient = self.the_world.map[(self.view_list[0])].plant_list[0]

        eat_quantity = 0
        if patient is not None:
            if patient.quantity >= 10:
                patient.quantity -= 10
                eat_quantity = 10
            if 0 <= patient.quantity < 10:
                eat_quantity = patient.quantity
                patient.quantity = 0

        self.drive_value_array[self.drive_index_dict['Energy']] += eat_quantity
        if self.drive_value_array[self.drive_index_dict['Energy']] > 100:
            self.drive_value_array[self.drive_index_dict['Energy']] = 100

    ############################################################################################################
    def procreate(self):

        patient = self.the_world.map[(self.view_list[2])].animal_list[0]

        if self.species == patient.species:
            if self.age >= config.Animal.childhood_length:
                if self.trait_value_dict['Sex'] != patient.trait_value_dict['Sex']:
                    if self.trait_value_dict['Sex'] == 'Female':
                        if random.uniform(0, 1) < config.Animal.pregnancy_chance:
                            self.get_pregnant(patient.genome)

    ############################################################################################################
    def update_drives(self):

        # the action taken, so we can enact its effects
        action_effect_dict = self.action_drive_change_dict[self.action_choice]

        # make a copy of the drives before we started


        # update the drives
        for i in range(self.num_drives):
            drive = self.drive_list[i]

            if drive == 'Energy':
                # metabolism and size effect how much energy things take
                self.drive_value_array[i] += self.current_size * action_effect_dict[drive] * self.metabolism
            else:
                self.drive_value_array[i] += action_effect_dict[drive]

        # drop health by the starvation rate
        if self.drive_value_array[self.drive_index_dict['Energy']] <= 0:
            self.drive_value_array[self.drive_index_dict['Health']] -= config.Animal.starvation_rate

        # cap all drives between 0 and 100
        for i in range(self.num_drives):
            if self.drive_value_array[i] < 0:
                self.drive_value_array[i] = 0
            if self.drive_value_array[i] > 100:
                self.drive_value_array[i] = 100

        # make a list of the drive changes for the current turn
        self.drive_value_change_array = self.drive_value_array - self.last_drive_value_array

    ############################################################################################################
    def update_neural_weights(self):

        self.get_sensory_representation()
        sensory_array = self.sensory_matrix.flatten()
        scaled_drive_value_array = self.drive_value_array/50 - 1
        print(scaled_drive_value_array)
        y = np.concatenate((sensory_array, scaled_drive_value_array, self.last_action_array, self.last_patient_array))

        self.neural_network_prediction_cost = self.neural_network.calc_cost(y, self.last_neural_output)
        self.neural_network_drive_cost = self.calculate_drive_cost()
        self.total_cost = self.neural_network_prediction_cost + self.neural_network_drive_cost

        self.neural_network.backpropogation(self.last_neural_input, y, self.last_neural_output,
                                            self.last_neural_hidden_state, self.total_cost)

    ############################################################################################################
    def calculate_drive_cost(self):
        current_learning_rates = np.zeros(self.num_drives)
        for i in range(self.num_drives):
            if self.drive_value_change_array[i] > 0:
                current_learning_rates[i] = self.trait_value_dict['Drive Reinforcement Rates'][0, i]
            elif self.drive_value_change_array[i] < 0:
                current_learning_rates[i] = self.trait_value_dict['Drive Reinforcement Rates'][1, i]
        weighted_drive_changes = current_learning_rates * self.drive_value_change_array
        sum_weighted_drive_changes = np.round(weighted_drive_changes.sum(), 5)

        drive_cost_array = np.zeros(self.output_size)
        action_index = self.a_indexes[0] + self.action_neuron_index_dict[self.action_choice]
        if sum_weighted_drive_changes > 0:
            good_move = 1
        else:
            good_move = 0

        drive_cost = 0.0
        if sum_weighted_drive_changes < 0:
            drive_cost = good_move - self.action_outputs[self.action_neuron_index_dict[self.action_choice]]
        elif sum_weighted_drive_changes > 0:
            drive_cost = good_move - self.action_outputs[self.action_neuron_index_dict[self.action_choice]]

        drive_cost_array[action_index] = drive_cost * np.absolute(sum_weighted_drive_changes)

        # print()
        # print("{:20s}".format("Action:"), self.action_choice)
        # print("{:20s}".format("Action Output:"), np.array2string(self.action_outputs[self.action_neuron_index_dict[self.action_choice]], formatter={'float_kind': lambda x: "%.3f" % x}))
        # print("{:20s}".format("Drive Values:"), np.array2string(self.drive_value_array, formatter={'float_kind': lambda x: "%.3f" % x}))
        # print("{:20s}".format("Drive Changes:"), np.array2string(self.drive_value_change_array, formatter={'float_kind': lambda x: "%.3f" % x}))
        # print("{:20s}".format("Learning Rates:"), np.array2string(current_learning_rates, formatter={'float_kind': lambda x: "%.3f" % x}))
        # print("{:20s}".format("Weighted Changes:"), np.array2string(weighted_drive_changes, formatter={'float_kind': lambda x: "%.5f" % x}), sum_weighted_drive_changes)
        # print("{:20s}".format("Good Move:"), good_move)
        # print("{:20s}".format("Drive Cost:"), "{:0.3f}".format(drive_cost))
        # print("{:20s}".format("Weighted Drive Cost:"), "{:0.6f}".format(drive_cost_array[action_index]))
        # print()

        return drive_cost_array

    ############################################################################################################
    def print_action_information(self):

        print("                              Rest      Attack    Eat      Procreate  Turn                Move")
        o = "{:25s}".format("Action Outputs")
        for output in self.action_outputs:
            o = o + " {:9.3f}".format(output)
        print(o)

        scaled_action_activations = self.action_outputs + abs(self.action_outputs.min()) + .00001
        o = "{:25s}".format("Scaled Action Outputs")
        for output in scaled_action_activations:
            o = o + " {:9.3f}".format(output)
        print(o)

        legal_action_array = self.get_legal_action_array()
        o = "{:25s}".format("Legal Action Outputs")
        for output in legal_action_array:
            o = o + " {:9.3f}".format(output)
        print(o)

        gated_action_activations = scaled_action_activations * legal_action_array
        o = "{:25s}".format("Gated Action Activity")
        for output in gated_action_activations:
            o = o + " {:9.3f}".format(output)
        print(o)

        legal_action_prob_distribution = gated_action_activations / gated_action_activations.sum()
        o = "{:25s}".format("Action Prob Distribution")
        for output in legal_action_prob_distribution:
            o = o + " {:9.3f}".format(output)
        print(o)

    ############################################################################################################
    def grow_older(self):
        self.age += 1

        if self.current_size < self.trait_value_dict['Max Size']:
            self.current_size += 1/config.Animal.childhood_length
            if self.current_size > self.trait_value_dict['Max Size']:
                self.current_size = self.trait_value_dict['Max Size']
            self.appearance[0] = self.current_size / 5

    ############################################################################################################
    def get_pregnant(self, father_genome):
        self.pregnant = 1
        self.father_genome = father_genome
        self.metabolism = config.Animal.pregnant_metabolism

    ############################################################################################################
    def bear_child(self):
        self.fetus.current_size = 0.1
        self.fetus.appearance[0] = self.fetus.current_size / 5
        self.fetus.age = 0
        self.pregnant = 0
        self.fetus = None
        self.metabolism = config.Animal.metabolism


############################################################################################################
############################################################################################################
class Mammal(Animal):
    def __init__(self, animal_id, mother_genome, father_genome):
        Animal.__init__(self, animal_id, mother_genome, father_genome)
        self.allowed_terrain_dict['Plains'] = True
        self.allowed_terrain_dict['Desert'] = True


############################################################################################################
############################################################################################################
class Lion(Mammal):
    def __init__(self, animal_id, mother_genome, father_genome):
        Mammal.__init__(self, animal_id, mother_genome, father_genome)
        self.species = 'Lion'
        self.image_dict = {0: 'assets/images/Lion0.gif', 90: 'assets/images/Lion90.gif',
                           180: 'assets/images/Lion180.gif', 270: 'assets/images/Lion270.gif'}
        self.attack_strength = 2
        self.diet_dict = {'Meat': 1}


############################################################################################################
############################################################################################################
class Zebra(Mammal):
    def __init__(self, animal_id, mother_genome, father_genome):
        Mammal.__init__(self, animal_id, mother_genome, father_genome)
        self.species = 'Zebra'
        self.image_dict = {0: 'assets/images/Zebra0.gif', 90: 'assets/images/Zebra90.gif',
                           180: 'assets/images/Zebra180.gif', 270: 'assets/images/Zebra270.gif'}
        self.diet_dict = {'Plants': 1}

import numpy as np
from src import config


############################################################################################################
############################################################################################################
class NervousSystem:
    ############################################################################################################
    def __init__(self, animal):
        ############################################################################################################
        self.animal = animal
        self.neural_network = None

        # the basic layer sizes
        self.h_size = None
        self.input_size = None
        self.output_size = None

        # the activation levels at each layer, and a copy of the activations from the previous turn
        self.neural_input = None
        self.neural_hidden_state = None
        self.neural_output = None
        self.last_neural_input = None
        self.last_neural_hidden_state = None
        self.last_neural_output = None

        # these, in addition to h_size, are the genetic parameters of the neural network
        self.p_learning_rate = None
        self.weight_init_stdev = None
        self.drive_direction_array = None
        self.drive_reinforcement_rate_matrix = None
        self.action_bias_array = None

        # variables for keeping track of the error at each time step
        self.neural_network_prediction_cost = None
        self.neural_network_drive_cost = None
        self.total_cost = None

        # this is the information for how the input and output layers are broken down
        # into sensory, drive, action, and action-argument subcomponents
        self.s_size = None
        self.d_size = None
        self.a_size = None
        self.aa_size = None
        self.s_indexes = None
        self.d_indexes = None
        self.a_indexes = None
        self.aa_indexes = None
        self.sensory_outputs = None
        self.drive_outputs = None
        self.action_outputs = None
        self.action_argument_outputs = None
        self.last_sensory_outputs = None
        self.last_drive_outputs = None
        self.last_action_outputs = None
        self.last_action_argument_outputs = None
        self.last_action_choice_array = None
        self.last_action_argument_choice_array = None

        # these are for the sensory processing
        self.view_list = None
        self.sensory_matrix = None
        self.tile_rep_size = None

        self.init_nervous_system()

    ############################################################################################################
    def init_nervous_system(self):

        self.p_learning_rate = self.animal.phenotype.trait_value_dict['Prediction Learning Rate']
        self.weight_init_stdev = self.animal.phenotype.trait_value_dict['Weight Init Stdev']
        self.drive_direction_array = self.animal.drive_system.drive_direction_array

        self.drive_reinforcement_rate_matrix = np.zeros([4, self.animal.drive_system.num_drives], float)
        trait_list = ['+ Learning Rate', '- Learning Rate', 'D+ Learning Rate', 'D- Learning Rate']
        for i in range(self.animal.drive_system.num_drives):
            drive = self.animal.drive_system.drive_list[i]
            for j in range(4):
                value = self.animal.phenotype.trait_value_dict[drive + trait_list[j]]
                self.drive_reinforcement_rate_matrix[j, i] = value

        self.action_bias_array = np.zeros([self.animal.action_system.num_actions], float)
        for i in range(self.animal.action_system.num_actions):
            trait = self.animal.action_system.action_list[i] + " Bias"
            self.action_bias_array[i] = self.animal.phenotype.trait_value_dict[trait]

        self.s_size = 5 * 4 * config.World.appearance_size
        self.d_size = self.animal.drive_system.num_drives
        self.a_size = self.animal.action_system.num_actions
        self.aa_size = config.World.appearance_size
        self.h_size = self.animal.phenotype.trait_value_dict['Num Hidden Neurons']

        self.s_indexes = (0, self.s_size - 1)
        self.d_indexes = (self.s_size, self.s_size + self.d_size - 1)
        self.a_indexes = (self.s_size + self.d_size, self.s_size + self.d_size + self.a_size - 1)
        self.aa_indexes = (self.s_size + self.d_size + self.a_size,
                           self.s_size + self.d_size + self.a_size + self.aa_size - 1)

        self.input_size = self.s_size + self.d_size + self.a_size + self.aa_size + self.h_size
        self.output_size = self.s_size + self.d_size + self.a_size + self.aa_size

        self.tile_rep_size = 4 * config.World.appearance_size
        self.last_neural_hidden_state = np.random.randn(self.h_size)

        self.last_action_choice_array = np.ones([self.a_size], float) * 0.5
        self.last_action_argument_outputs = np.ones([self.aa_size], float) * 0.5

        self.neural_network = NeuralNetwork(self.input_size, self.h_size, self.output_size,
                                            self.p_learning_rate,  self.weight_init_stdev)

    ############################################################################################################
    def __repr__(self):
        return "Nervous System: {}-{}-{}\n".format(self.input_size, self.h_size, self.output_size)

    ############################################################################################################
    def print_nervous_system(self):
        print(self, end='')
        print("     Learning Rate: {}".format(self.p_learning_rate))
        print("     Health Learning Rates: {}".format(self.p_learning_rate))
        print("     Learning Rate: {}".format(self.p_learning_rate))
        print("     Health Reinforcement: {} {} {}".format(self.drive_direction_array[0],
                                                           self.drive_reinforcement_rate_matrix[0, 0],
                                                           self.drive_reinforcement_rate_matrix[1, 0]))
        print("     Energy Reinforcement: {} {} {}".format(self.drive_direction_array[1],
                                                           self.drive_reinforcement_rate_matrix[0, 1],
                                                           self.drive_reinforcement_rate_matrix[1, 1]))
        print("     Arousal Reinforcement: {} {} {}".format(self.drive_direction_array[2],
                                                            self.drive_reinforcement_rate_matrix[0, 2],
                                                            self.drive_reinforcement_rate_matrix[1, 2]))
        for i in range(self.animal.action_system.num_actions):
            print("     {} Bias: {}".format(self.animal.action_system.action_list[i], self.action_bias_array[i]))

    ############################################################################################################
    def get_sensory_representation(self):
        self.get_view_list()
        rep_list = []
        for view in self.view_list:
            tile_rep_array = self.get_tile_representation(view)
            rep_list.append(tile_rep_array)
        self.sensory_matrix = np.array(rep_list)

    ############################################################################################################
    def get_view_list(self):
        x = self.animal.position[0]
        y = self.animal.position[1]

        if self.animal.orientation == 0:
            self.view_list = [(x, y), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x + 2, y)]
        elif self.animal.orientation == 90:
            self.view_list = [(x, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x, y - 2)]
        elif self.animal.orientation == 180:
            self.view_list = [(x, y), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x - 2, y)]
        elif self.animal.orientation == 270:
            self.view_list = [(x, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x, y + 2)]

    ############################################################################################################
    def get_tile_representation(self, tile_location):

        tile_representation_list = []
        x = tile_location[0]
        y = tile_location[1]

        if (x >= 0) and (y >= 0) and (x <= config.World.num_columns - 1) and (y <= config.World.num_rows - 1):
            tile_representation_list.append(self.animal.the_world.map[x, y].appearance)

            if len(self.animal.the_world.map[x, y].animal_list):
                tile_representation_list.append(self.animal.the_world.map[x, y].animal_list[0].appearance)
            else:
                tile_representation_list.append(self.animal.the_world.map[x, y].appearance)

            if len(self.animal.the_world.map[x, y].plant_list):
                tile_representation_list.append(self.animal.the_world.map[x, y].plant_list[0].appearance)
            else:
                tile_representation_list.append(self.animal.the_world.map[x, y].appearance)

            if len(self.animal.the_world.map[x, y].object_list):
                tile_representation_list.append(self.animal.the_world.map[x, y].object_list[0].appearance)
            else:
                tile_representation_list.append(self.animal.the_world.map[x, y].appearance)
        else:
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)
            tile_representation_list.append(np.ones([config.World.appearance_size]) * 0.5)

        tile_rep_array = np.array(tile_representation_list)

        return tile_rep_array

    ############################################################################################################
    def neural_feedforward(self):

        self.neural_input = np.concatenate((self.sensory_matrix.flatten(),
                                            self.animal.drive_system.drive_value_array,
                                            self.last_action_choice_array,
                                            self.last_action_argument_outputs,
                                            self.last_neural_hidden_state))

        self.neural_hidden_state, self.neural_output = self.neural_network.feedforward(self.neural_input)

        self.sensory_outputs = self.neural_output[self.s_indexes[0]:self.s_indexes[1] + 1]
        self.drive_outputs = self.neural_output[self.d_indexes[0]:self.d_indexes[1] + 1]
        self.action_outputs = self.neural_output[self.a_indexes[0]:self.a_indexes[1] + 1]
        self.action_argument_outputs = self.neural_output[self.aa_indexes[0]:self.aa_indexes[1] + 1]

    ############################################################################################################
    def update_neural_weights(self):

        self.last_neural_input = self.neural_input
        self.last_neural_output = self.neural_output
        self.last_action_choice_array = self.animal.action_system.action_choice_array
        self.last_action_argument_outputs = self.action_argument_outputs
        self.last_neural_hidden_state = self.neural_hidden_state

        self.get_sensory_representation()
        sensory_array = self.sensory_matrix.flatten()

        y = np.concatenate((sensory_array, self.animal.drive_system.drive_value_array,
                            self.last_action_choice_array, self.last_action_argument_outputs))

        self.neural_network_prediction_cost = self.neural_network.calc_cost(y, self.last_neural_output)
        self.total_cost = self.neural_network_prediction_cost
        self.neural_network.backpropogation(self.last_neural_input, self.last_neural_output,
                                            self.last_neural_hidden_state, self.total_cost)


############################################################################################################
############################################################################################################
class NeuralNetwork:
    ############################################################################################################
    def __init__(self, input_size, hidden_size, output_size, learning_rate, weight_init_stdev):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weight_init_stdev = weight_init_stdev

        self.h_bias = np.random.normal(0, self.weight_init_stdev, [self.hidden_size])
        self.h_x = np.random.normal(0, self.weight_init_stdev, [self.hidden_size, self.input_size])

        self.o_bias = np.random.normal(0, self.weight_init_stdev, [self.output_size])
        self.o_h = np.random.normal(0, self.weight_init_stdev, [self.output_size, self.hidden_size])

        self.learning_rate = learning_rate

    ############################################################################################################
    def feedforward(self, x):
        h = self.tanh(np.dot(self.h_x, x) + self.h_bias)
        o = self.sigmoid(np.dot(self.o_h, h) + self.o_bias)
        return h, o

    ############################################################################################################
    @staticmethod
    def calc_cost(y, o):
        return y - o
        # absolute value of the difference

    ############################################################################################################
    def backpropogation(self, x, o, h, o_cost):
        o_delta = o_cost * self.sigmoid_prime(o)

        h_cost = np.dot(o_delta, self.o_h)
        h_delta = h_cost * self.tanh_prime(h)

        # change all these to -=
        self.o_bias += o_delta * self.learning_rate
        self.o_h += (np.dot(o_delta.reshape(len(o_delta), 1), h.reshape(1, len(h))) * self.learning_rate)

        self.h_bias += h_delta * self.learning_rate
        self.h_x += (np.dot(h_delta.reshape(len(h_delta), 1), x.reshape(1, len(x))) * self.learning_rate)

    ############################################################################################################
    @staticmethod
    def tanh(z):
        return np.tanh(z)

    ############################################################################################################
    @staticmethod
    def tanh_prime(z):
        return 1.0 - np.tanh(z)**2

    ############################################################################################################
    @staticmethod
    def sigmoid(z):
        return 1/(1+np.exp(-z))

    ############################################################################################################
    @staticmethod
    def sigmoid_prime(z):
        return 1/(1+np.exp(-z)) * (1 - 1/(1+np.exp(-z)))

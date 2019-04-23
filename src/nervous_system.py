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
        self.input_size = None
        self.h_size = None
        self.output_size = None

        # the activation levels at each layer, and a copy of the activations from the previous turn
        self.neural_input_state = None
        self.neural_hidden_state = None
        self.neural_output_state = None

        # a separate place to keep track of the activity level for the different components of io
        self.sensory_inputs = None
        self.drive_inputs = None
        self.action_inputs = None
        self.action_argument_inputs = None
        self.sensory_outputs = None
        self.drive_outputs = None
        self.action_outputs = None
        self.action_argument_outputs = None

        # these, in addition to h_size, are the genetic parameters of the neural network
        self.p_learning_rate = None
        self.weight_init_stdev = None
        self.action_bias_array = None

        # the external information about drives and actions that the network uses
        self.drive_direction_array = None
        self.drive_reinforcement_rate_matrix = None
        self.drive_value_change = None

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
        self.last_h_indexes = None

        # these are for the sensory processing
        self.tile_rep_size = 4 * config.World.appearance_size
        self.view_list = None
        self.sensory_matrix = None
        self.sensory_array = None

        self.init_nervous_system()

    ############################################################################################################
    def __repr__(self):
        output_string = "Nervous System: {}-{}-{}\n".format(self.input_size, self.h_size, self.output_size)
        output_string += "    Prediction Learning Rate: {:0.5f}\n".format(self.p_learning_rate)
        output_string += "    Health Reinforcement:     {}   {:0.5f}   {:0.5f}\n".format(self.drive_direction_array[0],
                                                                           self.drive_reinforcement_rate_matrix[0, 0],
                                                                           self.drive_reinforcement_rate_matrix[1, 0])
        output_string += "    Energy Reinforcement:     {}   {:0.5f}   {:0.5f}\n".format(self.drive_direction_array[1],
                                                                           self.drive_reinforcement_rate_matrix[0, 1],
                                                                           self.drive_reinforcement_rate_matrix[1, 1])
        output_string += "    Arousal Reinforcement:    {}   {:0.5f}   {:0.5f}\n".format(self.drive_direction_array[2],
                                                                           self.drive_reinforcement_rate_matrix[0, 2],
                                                                           self.drive_reinforcement_rate_matrix[1, 2])
        output_string += "    Action Biases\n"
        for i in range(self.animal.action_system.num_actions):
            output_string += "        {:>12s}:     {}\n".format(self.animal.action_system.action_list[i],
                                                                self.action_bias_array[i])

        return output_string

    ############################################################################################################
    def init_nervous_system(self):

        # initialize the layer sizes
        self.h_size = self.animal.phenotype.trait_value_dict['Num Hidden Neurons']

        self.s_size = 5 * 4 * config.World.appearance_size
        self.d_size = self.animal.drive_system.num_drives
        self.a_size = self.animal.action_system.num_actions
        self.aa_size = config.World.appearance_size
        self.input_size = self.s_size + self.d_size + self.a_size + self.aa_size + self.h_size

        self.output_size = self.s_size + self.d_size + self.a_size + self.aa_size

        # get the specific indexes for the different
        self.s_indexes = (0, self.s_size - 1)
        self.d_indexes = (self.s_size, self.s_size + self.d_size - 1)
        self.a_indexes = (self.s_size + self.d_size, self.s_size + self.d_size + self.a_size - 1)
        self.aa_indexes = (self.s_size + self.d_size + self.a_size,
                           self.s_size + self.d_size + self.a_size + self.aa_size - 1)
        self.last_h_indexes = (self.s_size + self.d_size + self.a_size + self.aa_size,
                               self.s_size + self.d_size + self.a_size + self.aa_size + self.h_size - 1)

        # initial weight parameters
        self.weight_init_stdev = self.animal.phenotype.trait_value_dict['Weight Init Stdev']
        self.action_bias_array = np.zeros([self.animal.action_system.num_actions], float)
        for i in range(self.animal.action_system.num_actions):
            trait = self.animal.action_system.action_list[i] + " Bias"
            self.action_bias_array[i] = self.animal.phenotype.trait_value_dict[trait]

        # initialize learning rates
        self.p_learning_rate = self.animal.phenotype.trait_value_dict['Prediction Learning Rate']

        self.drive_direction_array = np.zeros([3], float)
        self.drive_direction_array[0] = self.animal.phenotype.trait_value_dict['Health Value Direction']
        self.drive_direction_array[1] = self.animal.phenotype.trait_value_dict['Energy Value Direction']
        self.drive_direction_array[2] = self.animal.phenotype.trait_value_dict['Arousal Value Direction']

        self.drive_reinforcement_rate_matrix = np.zeros([2, 3], float)
        self.drive_reinforcement_rate_matrix[0, 0] = self.animal.phenotype.trait_value_dict['Health Learning Rate']
        self.drive_reinforcement_rate_matrix[1, 0] = self.animal.phenotype.trait_value_dict['HealthD Learning Rate']
        self.drive_reinforcement_rate_matrix[0, 1] = self.animal.phenotype.trait_value_dict['Energy Learning Rate']
        self.drive_reinforcement_rate_matrix[1, 1] = self.animal.phenotype.trait_value_dict['EnergyD Learning Rate']
        self.drive_reinforcement_rate_matrix[0, 2] = self.animal.phenotype.trait_value_dict['Arousal Learning Rate']
        self.drive_reinforcement_rate_matrix[1, 2] = self.animal.phenotype.trait_value_dict['ArousalD Learning Rate']

        self.neural_network = NeuralNetwork(self.input_size, self.h_size, self.output_size, self.weight_init_stdev)
        self.neural_network.o_bias[self.a_indexes[0]:self.a_indexes[1]+1] = self.action_bias_array

        # initialize layer activations for recurrency
        self.neural_hidden_state = np.random.normal(0, 0.001, self.h_size)
        self.neural_input_state = np.ones(self.input_size) * 0.5
        self.neural_output_state = np.ones(self.output_size) * 0.5

    ############################################################################################################
    def update_sensory_state(self):
        self.view_list = self.get_view_list()
        self.sensory_matrix = self.get_sensory_representation()
        self.sensory_array = self.sensory_matrix.flatten()

    ############################################################################################################
    def get_sensory_representation(self):
        view_list = self.get_view_list()
        rep_list = []
        for view in view_list:
            tile_rep_array = self.get_tile_representation(view)
            rep_list.append(tile_rep_array)
        sensory_matrix = np.array(rep_list)
        return sensory_matrix

    ############################################################################################################
    def get_view_list(self):
        x = self.animal.position[0]
        y = self.animal.position[1]
        view_list = None
        if self.animal.orientation == 0:
            view_list = [(x, y), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x + 2, y)]
        elif self.animal.orientation == 90:
            view_list = [(x, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x, y - 2)]
        elif self.animal.orientation == 180:
            view_list = [(x, y), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x - 2, y)]
        elif self.animal.orientation == 270:
            view_list = [(x, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x, y + 2)]
        return view_list

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
        neural_input_state = np.concatenate((self.sensory_array,
                                             self.animal.drive_system.drive_value_array,
                                             self.animal.action_system.action_choice_array,
                                             self.animal.action_system.action_argument_choice_array,
                                             self.neural_hidden_state))
        neural_hidden_state, neural_output_state = self.neural_network.feedforward(self.neural_input_state)
        return neural_input_state, neural_hidden_state, neural_output_state

    ############################################################################################################
    def stored_neural_feedforward(self):
        self.update_sensory_state()
        neural_input_state, neural_hidden_state, neural_output_state = self.neural_feedforward()

        self.neural_input_state = neural_input_state
        self.neural_hidden_state = neural_hidden_state
        self.neural_output_state = neural_output_state

        self.sensory_outputs = self.neural_output_state[self.s_indexes[0]:self.s_indexes[1] + 1]
        self.drive_outputs = self.neural_output_state[self.d_indexes[0]:self.d_indexes[1] + 1]
        self.action_outputs = self.neural_output_state[self.a_indexes[0]:self.a_indexes[1] + 1]
        self.action_argument_outputs = self.neural_output_state[self.aa_indexes[0]:self.aa_indexes[1] + 1]

    ############################################################################################################
    def update_neural_weights(self):
        # these are the outputs of the previous feedforward
        y_predicted = np.concatenate((self.sensory_outputs, self.drive_outputs, self.action_outputs,
                                      self.action_argument_outputs))

        y_actual = np.concatenate((self.sensory_array, self.animal.drive_system.drive_value_array,
                                   self.animal.action_system.action_choice_array, self.action_argument_outputs))

        self.neural_network_prediction_cost = self.neural_network.calc_cost(y_actual, y_predicted)
        self.neural_network.backpropogation(self.neural_input_state, y_predicted, self.neural_hidden_state,
                                            self.neural_network_prediction_cost, self.p_learning_rate)


############################################################################################################
############################################################################################################
class NeuralNetwork:
    ############################################################################################################
    def __init__(self, input_size, hidden_size, output_size, weight_init_stdev):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weight_init_stdev = weight_init_stdev

        self.h_bias = np.random.normal(0, self.weight_init_stdev, [self.hidden_size])
        self.h_x = np.random.normal(0, self.weight_init_stdev, [self.hidden_size, self.input_size])

        self.o_bias = np.random.normal(0, self.weight_init_stdev, [self.output_size])
        self.o_h = np.random.normal(0, self.weight_init_stdev, [self.output_size, self.hidden_size])

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
    def backpropogation(self, x, o, h, o_cost, learning_rate):
        o_delta = o_cost * self.sigmoid_prime(o)

        h_cost = np.dot(o_delta, self.o_h)
        h_delta = h_cost * self.tanh_prime(h)

        # change all these to -=
        self.o_bias += o_delta * learning_rate
        self.o_h += (np.dot(o_delta.reshape(len(o_delta), 1), h.reshape(1, len(h))) * learning_rate)

        self.h_bias += h_delta * learning_rate
        self.h_x += (np.dot(h_delta.reshape(len(h_delta), 1), x.reshape(1, len(x))) * learning_rate)

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

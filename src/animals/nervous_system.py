import numpy as np
from src import config
from src.animals.neural_network import NeuralNetwork


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
        self.drive_target_array = None
        self.drive_change_target_array = None
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
        output_string += "    Health Reinforcement:     {}   {:0.5f}   {:0.5f}\n".format(self.drive_target_array[0],
                                                                           self.drive_reinforcement_rate_matrix[0, 0],
                                                                           self.drive_reinforcement_rate_matrix[1, 0])
        output_string += "    Energy Reinforcement:     {}   {:0.5f}   {:0.5f}\n".format(self.drive_target_array[1],
                                                                           self.drive_reinforcement_rate_matrix[0, 1],
                                                                           self.drive_reinforcement_rate_matrix[1, 1])
        output_string += "    Arousal Reinforcement:    {}   {:0.5f}   {:0.5f}\n".format(self.drive_target_array[2],
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

        # initialize prediction learning rate
        self.p_learning_rate = self.animal.phenotype.trait_value_dict['Prediction Learning Rate']

        # initialize drive targets
        self.drive_target_array = np.zeros([self.animal.drive_system.num_drives], float)
        for i in range(self.animal.drive_system.num_drives):
            target_string = self.animal.drive_system.drive_list[i] + " Value Target"
            self.drive_target_array[i] = self.animal.phenotype.trait_value_dict[target_string]

        # initialize drive target and drive change target learning rates
        self.drive_reinforcement_rate_matrix = np.zeros([2, self.animal.drive_system.num_drives], float)
        for i in range(self.animal.drive_system.num_drives):
            target_string = self.animal.drive_system.drive_list[i] + " Learning Rate"
            target_change_string = self.animal.drive_system.drive_list[i] + "D Learning Rate"
            self.drive_reinforcement_rate_matrix[0, i] = self.animal.phenotype.trait_value_dict[target_string]
            self.drive_reinforcement_rate_matrix[1, i] = self.animal.phenotype.trait_value_dict[target_change_string]

        # create the neural network
        self.neural_network = NeuralNetwork(self.input_size, self.h_size, self.output_size, self.weight_init_stdev)

        # initialize innate biases
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

        if config.Debug.nervous_system:
            print("\nSensory State:")
            print("    Position & Orientation:", self.animal.position, self.animal.orientation)
            print("    Sensory Matrix:", self.sensory_matrix.shape)
            for i in range(self.sensory_matrix.shape[0]):
                print("    Tile", self.view_list[i])
                print("        terrain:", np.array2string(self.sensory_matrix[i, 0, :],
                                                          precision=2,
                                                          floatmode='maxprec',
                                                          separator=' ',
                                                          suppress_small=True))
                print("        animal:", np.array2string(self.sensory_matrix[i, 1, :],
                                                         precision=2,
                                                         floatmode='maxprec',
                                                         separator=' ',
                                                         suppress_small=True))
                print("        plant:", np.array2string(self.sensory_matrix[i, 2, :],
                                                        precision=2,
                                                        floatmode='maxprec',
                                                        separator=' ',
                                                        suppress_small=True))
                print("        object:", np.array2string(self.sensory_matrix[i, 3, :],
                                                         precision=2,
                                                         floatmode='maxprec',
                                                         separator=' ',
                                                         suppress_small=True))
            print("    Sensory Array:", self.sensory_array.shape)
            print("\n")

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

        for i in range(self.animal.drive_system.num_drives):
            drive_value_cost_array, drive_change_cost_array = self.calculate_drive_costs(i)
            drive_value_learning_rate = self.drive_reinforcement_rate_matrix[0, i]
            drive_change_learning_rate = self.drive_reinforcement_rate_matrix[1, i]

            self.neural_network.backpropogation(self.neural_input_state, y_predicted, self.neural_hidden_state,
                                                drive_value_cost_array, drive_value_learning_rate)

            self.neural_network.backpropogation(self.neural_input_state, y_predicted, self.neural_hidden_state,
                                                drive_change_cost_array, drive_change_learning_rate)

    ############################################################################################################
    def calculate_drive_costs(self, drive_index):

        action_choice = self.animal.action_system.action_choice
        action_index = self.animal.action_system.action_index_dict[action_choice]
        full_action_index = action_index + self.a_indexes[0]

        drive = self.animal.drive_system.drive_list[drive_index]

        drive_value = self.animal.drive_system.drive_value_array[drive_index]
        drive_value_target = self.drive_target_array[drive_index]
        drive_value_error = drive_value_target - drive_value
        drive_value_cost = -1 * abs(drive_value_error)
        drive_value_cost_array = np.zeros(self.output_size)
        drive_value_cost_array[full_action_index] = drive_value_cost

        drive_change = self.animal.drive_system.drive_value_array[drive_index] - self.animal.drive_system.last_drive_value_array[drive_index]
        drive_change_target = drive_value_error
        drive_change_error = drive_change_target - drive_change
        drive_change_cost = -1 * abs(drive_change_error)
        drive_change_cost_array = np.zeros(self.output_size)
        drive_change_cost_array[full_action_index] = drive_change_cost

        #print("\n" + drive)
        #print("Value: {:0.4f}    Goal: {:0.4f}   Error: {:0.3f}   Cost: {:0.3f}".format(drive_value, drive_value_target, drive_value_error, drive_value_cost))
        #print("Change: {:0.4f}   Goal: {:0.4f}   Error: {:0.3f}   Cost: {:0.3f}".format(drive_change, drive_change_target, drive_change_error, drive_change_cost))

        return drive_value_cost_array, drive_change_cost_array


############################################################################################################
############################################################################################################


from src import config
import numpy as np
import random


############################################################################################################
############################################################################################################
class ActionSystem:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal

        self.num_actions = None  # the total number of actions available
        self.action_list = None  # the list of actions available
        self.action_index_dict = None  # an index dict for all actions

        self.action_outputs = None  # the activity of all action units in the neural network output layer
        self.legal_action_array = None  # a binary array stating which actions are legal on the current turn
        self.gated_action_activations = None  # previous 2 multiplied together, zeroing out activity of illegal actions
        self.legal_action_prob_distribution = None  # previous turned into a prob distribution

        self.action_choice = None  # the action string that is chosen on the current turn
        self.action_choice_array = None  # a one-hot binary array showing the action taken this turn
        self.action_argument_outputs = None  # the activation of the patient output neurons

        self.action_drive_change_dict = config.Animal.action_drive_change_dict

        self.init_actions()

    ############################################################################################################
    def __repr__(self):
        return "Action System: {} Actions\n".format(self.num_actions)

    ############################################################################################################
    def init_actions(self):

        self.num_actions = 0
        self.action_list = []
        self.action_index_dict = {}

        for action in self.action_drive_change_dict:
            self.action_list.append(action)
            self.action_index_dict[action] = self.num_actions
            self.num_actions += 1

    ############################################################################################################
    def print_action_system(self):
        print(self, end='')
        for action in self.action_list:
            print("     ", action)

    ############################################################################################################
    def print_action_activations(self):
        print(self, end='')
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
    def get_legal_action_probabilities(self):
        a_act = self.animal.nervous_system.action_outputs + .01

        self.legal_action_array = self.get_legal_action_array()
        self.gated_action_activations = a_act * self.legal_action_array
        self.legal_action_prob_distribution = self.gated_action_activations / self.gated_action_activations.sum()

    ############################################################################################################
    def get_legal_action_array(self):

        legal_action_array = np.zeros([self.num_actions])

        # Resting and turning are always legal
        legal_action_array[self.action_index_dict['Rest']] = 1
        legal_action_array[self.action_index_dict['Turn']] = 1

        # if forward tile not allowable for species type, make move illegal
        forward_terrain_type = self.animal.the_world.map[self.animal.nervous_system.view_list[2]].terrain_type
        forward_animal_list = self.animal.the_world.map[self.animal.nervous_system.view_list[2]].animal_list
        current_plant_list = self.animal.the_world.map[self.animal.nervous_system.view_list[2]].plant_list
        current_object_list = self.animal.the_world.map[self.animal.nervous_system.view_list[2]].object_list

        if self.animal.allowed_terrain_dict[forward_terrain_type]:
            legal_action_array[self.action_index_dict['Move']] = 1

        if len(forward_animal_list):
            legal_action_array[self.action_index_dict['Attack']] = 1
            legal_action_array[self.action_index_dict['Procreate']] = 1
            legal_action_array[self.action_index_dict['Move']] = 0

        # if not plant or object in current tile, make eat illegal
        if "Plants" in self.animal.diet_dict:
            if len(current_plant_list):
                legal_action_array[self.action_index_dict['Eat']] = 1

        if "Meat" in self.animal.diet_dict:
            if len(current_object_list):
                if current_object_list[0].object_type == "Meat":
                    legal_action_array[self.action_index_dict['Eat']] = 1

        return legal_action_array

    ############################################################################################################
    def choose_action(self):
        action_choice_cumulative_probabilities = []
        cumulative_probability_sum = 0
        action_choice = None
        action_choice_number = random.random()
        for i in range(self.num_actions):
            if self.legal_action_prob_distribution[i]:
                cumulative_probability_sum += self.legal_action_prob_distribution[i]
                action_choice_cumulative_probabilities.append(cumulative_probability_sum)
                if action_choice_number < cumulative_probability_sum:
                    action_choice = self.action_list[i]
                    break
        self.action_choice = action_choice
        self.action_choice_array = np.zeros([self.num_actions], float)
        self.action_choice_array[self.action_index_dict[self.action_choice]] = 1

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

        x = self.animal.position[0]
        y = self.animal.position[1]

        new_x = x
        new_y = y
        if self.animal.orientation == 0:
            new_x = x + 1
        elif self.animal.orientation == 90:
            new_y = y - 1
        elif self.animal.orientation == 180:
            new_x = x - 1
        elif self.animal.orientation == 270:
            new_y = y + 1

        self.animal.position = [new_x, new_y]

        self.animal.the_world.map[(x, y)].animal_list.pop()
        self.animal.the_world.map[(new_x, new_y)].animal_list.append(self)

    ############################################################################################################
    def turn(self):
        turn_amount_mod = self.animal.nervous_system.action_argument_outputs.mean()

        if 0.167 <= turn_amount_mod <= 0.5:
            self.animal.orientation += 270

        elif 0.5 <= turn_amount_mod <= 0.833:
            self.animal.orientation += 90

        elif turn_amount_mod < 0.167 or turn_amount_mod > 0.833:
            self.animal.orientation += 180

        if self.animal.orientation >= 360:
            self.animal.orientation -= 360

    ############################################################################################################
    def attack(self):
        forward_tile = self.animal.nervous_system.view_list[2]
        patient = self.animal.the_world.map[forward_tile].animal_list[0]
        patient.drive_system.drive_value_array[patient.drive_index_dict['Health']] -= \
            self.animal.attack_strength * self.animal.current_size
        self.animal.drive_system.drive_value_array[patient.drive_index_dict['Health']] -= \
            patient.attack_strength * patient.current_size

    ############################################################################################################
    def eat(self):
        patient = None
        local_plant_list = self.animal.the_world.map[(self.animal.nervous_system.view_list[0])].plant_list
        local_object_list = self.animal.the_world.map[(self.animal.nervous_system.view_list[0])].object_list
        eat_quantity = 0

        if "Meat" in self.animal.diet_dict:
            if len(local_object_list):
                if local_object_list[0].object_type == 'Meat':
                    patient = local_object_list[0]

        if "Plants" in self.animal.diet_dict:
            if len(local_plant_list):
                patient = local_plant_list[0]

        if patient is not None:
            if patient.quantity >= 10:
                patient.quantity -= 10
                eat_quantity = 10
            if 0 <= patient.quantity < 10:
                eat_quantity = patient.quantity
                patient.quantity = 0

        self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']] += eat_quantity
        if self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']] > 100:
            self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']] = 100

    ############################################################################################################
    def procreate(self):

        patient = self.animal.the_world.map[(self.animal.nervous_system.view_list[2])].animal_list[0]

        if self.animal.species == patient.species:
            if self.animal.phenotype.trait_value_dict['Sex'] != patient.phenotype.trait_value_dict['Sex']:
                if random.random() < config.Animal.pregnancy_chance:
                    if self.animal.phenotype.trait_value_dict['Sex'] == 1:
                        if self.animal.age >= config.Animal.childhood_length:
                            if self.animal.pregnant == 0:
                                self.animal.get_pregnant(patient.genome)
                    if patient.phenotype.trait_value_dict['Sex'] == 1:
                        if patient.age >= config.Animal.childhood_length:
                            if patient.pregnant == 0:
                                patient.get_pregnant(self.animal.genome)

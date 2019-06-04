from src import config
import numpy as np
import random


class ActionSystem:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal

        self.num_actions = None  # the total number of actions available
        self.action_list = None  # the list of actions available
        self.action_index_dict = None  # an index dict for all actions

        self.action_outputs = None   # the output layer action activations of the neural network
        self.legal_action_array = None  # a binary array stating which actions are legal on the current turn
        self.gated_action_activations = None  # previous 2 multiplied together, zeroing out activity of illegal actions
        self.legal_action_prob_distribution = None  # previous turned into a prob distribution

        self.action_choice = None  # the action string that is chosen on the current turn
        self.action_choice_array = None  # a one-hot binary array showing the action taken this turn

        self.action_argument_outputs = None
        self.action_argument_choice_array = None

        self.action_drive_change_dict = config.Animal.action_drive_change_dict

        self.init_actions()

    ############################################################################################################
    def __repr__(self):
        output_string = "Action System: {} Actions\n".format(self.num_actions)
        input_state, hidden_state, output_state = self.animal.nervous_system.neural_feedforward()
        action_outputs = output_state[self.animal.nervous_system.a_indexes[0]:
                                      self.animal.nervous_system.a_indexes[1] + 1]

        for i in range(self.num_actions):
            output_string += "    {:12s}: {:0.3f}  {}  {:0.3f}  {:0.3f}  {}\n".format(self.action_list[i],
                                                                                     action_outputs[i],
                                                                                     self.legal_action_array[i],
                                                                                     self.gated_action_activations[i],
                                                                                     self.legal_action_prob_distribution[i],
                                                                                     self.action_choice_array[i])
        return output_string

    ############################################################################################################
    def init_actions(self):

        self.num_actions = 0
        self.action_list = []
        self.action_index_dict = {}

        for action in self.action_drive_change_dict:
            self.action_list.append(action)
            self.action_index_dict[action] = self.num_actions
            self.num_actions += 1

        self.action_choice_array = np.ones([self.num_actions], float) * 0.5
        self.action_argument_choice_array = np.ones([30], float) * 0.5
        self.action_outputs = np.ones([30], float) * 0.5

    ############################################################################################################
    def action_turn(self):
        self.get_legal_action_probabilities()
        self.choose_action()
        self.take_action()

    ############################################################################################################
    def get_legal_action_probabilities(self, action_outputs=None):
        noise = self.animal.phenotype.trait_value_dict['Action Noise']

        if action_outputs is None:
            a_act = self.animal.nervous_system.action_outputs + noise
        else:
            a_act = action_outputs + noise

        self.action_outputs = a_act

        for i in range(len(a_act)):
            if a_act[i] > 1.0:
                a_act[i] = 1.0

        self.legal_action_array = self.get_legal_action_array()
        self.gated_action_activations = a_act * self.legal_action_array
        self.legal_action_prob_distribution = self.gated_action_activations / self.gated_action_activations.sum()

        if config.Debug.action_system:
            print("\n{} {} Legal Action Probabilities".format(self.animal.species, self.animal.id_number))
            for i in range(self.num_actions):
                print("    {:9s}: {:0.3f} {} {:0.3f} {:0.3f}".format(self.action_list[i],
                                                                     a_act[i],
                                                                     self.legal_action_array[i],
                                                                     self.gated_action_activations[i],
                                                                     self.legal_action_prob_distribution[i]))
            print("\n")

    ############################################################################################################
    def get_legal_action_array(self):

        legal_action_array = np.zeros([self.num_actions])

        # Resting and turning are always legal
        legal_action_array[self.action_index_dict['Rest']] = 1
        legal_action_array[self.action_index_dict['Turn']] = 1

        # if forward tile not allowable for species type, make move illegal
        view_list = self.animal.nervous_system.get_view_list()
        forward_terrain_type = self.animal.the_world.map[view_list[2]].terrain_type
        forward_animal_list = self.animal.the_world.map[view_list[2]].animal_list

        current_plant_list = self.animal.the_world.map[view_list[0]].plant_list
        current_object_list = self.animal.the_world.map[view_list[0]].object_list

        if self.animal.allowed_terrain_dict[forward_terrain_type]:
            legal_action_array[self.action_index_dict['Move']] = 1

        if len(forward_animal_list):
            legal_action_array[self.action_index_dict['Attack']] = 1
            legal_action_array[self.action_index_dict['Procreate']] = 1
            legal_action_array[self.action_index_dict['Move']] = 0

        # if not plant or object in current tile, make eat illegal
        if len(current_plant_list) > 0 or len(current_object_list) > 0:
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

        if config.Debug.action_system:
            print("\n{} {} Action Choice".format(self.animal.species, self.animal.id_number))
            print("    Action Choice Value", action_choice_number)

            cumulative_probability_sum = 0
            for i in range(self.num_actions):
                cumulative_probability_sum += self.legal_action_prob_distribution[i]
                if self.legal_action_prob_distribution[i]:
                    print("    {:9s}: {:0.3f} {:0.3f}".format(self.action_list[i],
                                                              self.legal_action_prob_distribution[i],
                                                              cumulative_probability_sum))
                else:
                    print("    {:9s}: {:0.3f} {:0.3f}".format(self.action_list[i],
                                                              self.legal_action_prob_distribution[i],
                                                              0))
            print("    Action Choice: ", action_choice)
            print("    Action Choice Array:", self.action_choice_array)
            print("\n")

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
        self.action_argument_choice_array = self.animal.nervous_system.action_argument_outputs

        if config.Debug.action_system:
            print("\n{} {} Action: Rest\n".format(self.animal.species, self.animal.id_number))

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
        self.animal.the_world.map[(new_x, new_y)].animal_list.append(self.animal)

        self.action_argument_choice_array = self.animal.nervous_system.action_argument_outputs

        if config.Debug.action_system:
            print("\n{} {} Action: Move".format(self.animal.species, self.animal.id_number))
            print("    Old Position:", x, y)
            print("    Orientation:", self.animal.orientation)
            print("    New Position:", self.animal.position[0], self.animal.position[1], "\n")

    ############################################################################################################
    def turn(self):

        turn_amount_mod = self.animal.nervous_system.action_argument_outputs.mean()
        old_orientation = self.animal.orientation

        if 0.167 <= turn_amount_mod <= 0.5:
            self.animal.orientation += 270

        elif 0.5 <= turn_amount_mod <= 0.833:
            self.animal.orientation += 90

        elif turn_amount_mod < 0.167 or turn_amount_mod > 0.833:
            self.animal.orientation += 180

        if self.animal.orientation >= 360:
            self.animal.orientation -= 360

        self.action_argument_choice_array = self.animal.nervous_system.action_argument_outputs

        if config.Debug.action_system:
            print("\n{} {} Action: Turn".format(self.animal.species, self.animal.id_number))
            print("    Turn Amount Mod:", turn_amount_mod)
            print("    Orientation:", old_orientation, self.animal.orientation, "\n")

    ############################################################################################################
    def attack(self):
        forward_tile = self.animal.nervous_system.view_list[2]
        defender = self.animal.the_world.map[forward_tile].animal_list[0]
        attacker = self.animal

        attacker_strength = attacker.attack_strength * attacker.current_size
        defender_strength = defender.attack_strength * defender.current_size

        damage_to_defender = attacker_strength/100
        defender_start_health = defender.drive_system.drive_value_array[defender.drive_system.drive_index_dict['Health']]
        defender.drive_system.drive_value_array[defender.drive_system.drive_index_dict['Health']] -= damage_to_defender
        defender_end_health = defender.drive_system.drive_value_array[defender.drive_system.drive_index_dict['Health']]

        damage_to_attacker = defender_strength/100
        attacker_start_health = self.animal.drive_system.drive_value_array[defender.drive_system.drive_index_dict['Health']]
        self.animal.drive_system.drive_value_array[defender.drive_system.drive_index_dict['Health']] -= damage_to_attacker
        attacker_end_health = self.animal.drive_system.drive_value_array[defender.drive_system.drive_index_dict['Health']]

        if defender.num_visible_features < 30:
            self.action_argument_choice_array = np.zeros([30])
            for i in range(defender.num_visible_features):
                self.action_argument_choice_array[i] = defender.appearance[i]
        elif defender.num_visible_features > 30:
            self.action_argument_choice_array = defender.appearance[:30]
        else:
            self.action_argument_choice_array = defender.appearance

        if config.Debug.action_system:
            print("\n{} {} Action: Attack!".format(self.animal.species, self.animal.id_number))
            print("    {} {} Attack!".format(self.animal.species, self.animal.id_number))
            print("    Attacker: {} {}   Size: {:0.3f}    Attack Strength: {}".format(self.animal.species,
                                                                                      self.animal.id_number,
                                                                                      self.animal.current_size,
                                                                                      attacker_strength))
            print("    Defender: {} {}   Size: {:0.3f}    Attack Strength: {}".format(defender.species,
                                                                                      defender.id_number,
                                                                                      defender.current_size,
                                                                                      defender_strength))
            print("    Attacker dealt {} damage, defender health {} to {}".format(damage_to_defender,
                                                                                  defender_start_health,
                                                                                  defender_end_health))
            print("    Defender dealt {} damage, attacker health {} to {}\n".format(damage_to_attacker,
                                                                                  attacker_start_health,
                                                                                  attacker_end_health))

    ############################################################################################################
    def eat(self):
        local_plant_list = self.animal.the_world.map[(self.animal.nervous_system.view_list[0])].plant_list
        local_object_list = self.animal.the_world.map[(self.animal.nervous_system.view_list[0])].object_list
        start_energy = self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']]
        digest_meat = self.animal.phenotype.trait_value_dict['Digest Meat']
        digest_plants = self.animal.phenotype.trait_value_dict['Digest Plants']
        sharp_teeth = self.animal.phenotype.trait_value_dict['Sharp Teeth']

        # if there is a meat object, determine how much energy the animal would get from eating it
        if len(local_object_list):

            local_object_kind = local_object_list[0].kind

            if local_object_kind == 'Meat':
                if local_object_list[0].quantity >= 10:
                    meat_quantity = 10
                else:
                    meat_quantity = local_object_list[0].quantity

                object_energy_value = meat_quantity * config.Animal.meat_energy * digest_meat * sharp_teeth
            else:
                object_energy_value = 0
                meat_quantity = 0
        else:
            object_energy_value = 0
            meat_quantity = 0

        # if there is a plant object, determine how much energy the animal would get from eating it
        if len(local_plant_list):
            if local_plant_list[0].quantity >= 10:
                plant_quantity = 10
            else:
                plant_quantity = local_plant_list[0].quantity

            plant_energy_value = plant_quantity * config.Animal.plant_energy * digest_plants * (1 - sharp_teeth)
        else:
            plant_quantity = 0
            plant_energy_value = 0

        # eat the one that gives more energy, if either give energy
        if object_energy_value or plant_energy_value:
            if object_energy_value > plant_energy_value:
                energy_gain = object_energy_value / 100
                local_object_list[0].quantity -= meat_quantity
                self.action_argument_choice_array = local_object_list[0].appearance
                patient = 'meat'
                eat_quantity = meat_quantity
            else:
                energy_gain = plant_energy_value / 100
                local_plant_list[0].quantity -= plant_quantity
                self.action_argument_choice_array = local_plant_list[0].appearance
                patient = 'grass'
                eat_quantity = plant_quantity
        else:
            energy_gain = 0
            patient = 'none'
            self.action_argument_choice_array = np.zeros([30])
            eat_quantity = 0

        self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']] += energy_gain
        if self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']] > 1.0:
            self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']] = 1.0

        if config.Debug.action_system:
            print("\n{} {} Action: Eat".format(self.animal.species, self.animal.id_number))
            print("    Start Energy:", start_energy)
            print("    Plants:", len(local_plant_list), plant_energy_value, plant_quantity, config.Animal.plant_energy, digest_plants, (1 - sharp_teeth))
            print("    Object:", len(local_object_list), object_energy_value, meat_quantity, config.Animal.meat_energy, digest_meat, sharp_teeth)
            print("    Patient:", patient, eat_quantity)
            print("    Energy Gain:", energy_gain)
            print("    End Energy:", self.animal.drive_system.drive_value_array[self.animal.drive_system.drive_index_dict['Energy']])
            print("\n")

    ############################################################################################################
    def procreate(self):

        partner = self.animal.the_world.map[(self.animal.nervous_system.view_list[2])].animal_list[0]
        new_pregnancy = False
        prob = random.random()

        if self.animal.species == partner.species:
            if self.animal.phenotype.trait_value_dict['Sex'] != partner.phenotype.trait_value_dict['Sex']:
                if prob < config.Animal.pregnancy_chance:
                    if self.animal.phenotype.trait_value_dict['Sex'] == 1:
                        if self.animal.age >= config.Animal.childhood_length:
                            if self.animal.pregnant == 0:
                                self.animal.get_pregnant(partner.genome)
                                new_pregnancy = True
                    if partner.phenotype.trait_value_dict['Sex'] == 1:
                        if partner.age >= config.Animal.childhood_length:
                            if partner.pregnant == 0:
                                partner.get_pregnant(self.animal.genome)
                                new_pregnancy = True

        if partner.num_visible_features < 30:
            self.action_argument_choice_array = np.zeros([30])
            for i in range(partner.num_visible_features):
                self.action_argument_choice_array[i] = partner.appearance[i]
        elif partner.num_visible_features > 30:
            self.action_argument_choice_array = partner.appearance[:30]
        else:
            self.action_argument_choice_array = partner.appearance

        if config.Debug.action_system:
            print("\n{} {} Action: Procreate".format(self.animal.species, self.animal.id_number))
            print("    Animal:", self.animal.species,
                  self.animal.id_number,
                  self.animal.phenotype.trait_value_dict['Sex'],
                  self.animal.age,
                  partner.pregnant)
            print("    Partner:", partner.species,
                  partner.id_number,
                  partner.phenotype.trait_value_dict['Sex'],
                  partner.age,
                  partner.pregnant)
            print("    Prob & Threshold:", prob, config.Animal.pregnancy_chance)
            print("    New Pregnancy: ", new_pregnancy, "\n")

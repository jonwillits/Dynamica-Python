import random
import numpy as np
from src import config
from src.animals import phenotype, drive_system, nervous_system, action_system, genome
import time


class Animal:
    ############################################################################################################
    def __init__(self, the_world, mother_genome=None, father_genome=None):
        ############################################################################################################
        self.the_world = the_world  # a reference to the world data structure
        self.kingdom = "Animal"  # this animal's kingdom type (ie plant or animal)
        self.species = None  # this animal's species type
        self.graphic_object = None  # this animal's graphic object, currently a python turtle object
        self.dead_graphic_object = None
        self.id_number = the_world.entity_counter  # a unique id number
        self.the_world.entity_counter += 1
        self.mother_genome = mother_genome
        self.father_genome = father_genome

        ############################################################################################################
        self.genome = None
        self.phenotype = None
        self.drive_system = None
        self.action_system = None
        self.nervous_system = None

        ############################################################################################################
        self.appearance = None
        self.visible_feature_label_list = None
        self.visible_feature_label_index_dict = None
        self.num_visible_features = None

        ############################################################################################################
        self.age = 0
        self.current_size = 0.1  # the animal's current size, global range 0-5, actual range specified genetically
        self.position = None    # the animal's coordinates
        self.orientation = random.choice([0, 90, 180, 270])  # can make this nonrandom later
        self.metabolism = config.Animal.metabolism
        self.attack_strength = None

        ############################################################################################################
        self.pregnant = 0
        self.baby_daddy_genome = None
        self.fetus = None

    ############################################################################################################
    def __repr__(self):
        output_string = "{} {}\n".format(self.species, self.id_number)
        output_string += "    Position:     {}\n".format(self.position)
        output_string += "    Orientation:  {}\n".format(self.orientation)
        output_string += "    Age:          {}\n".format(self.age)
        output_string += "    Current Size: {}\n".format(self.current_size)
        output_string += "    Sex:          {}\n".format(self.phenotype.trait_value_dict['Sex'])
        output_string += "    Pregnant:     {}\n".format(self.pregnant)
        return output_string

    ############################################################################################################
    def init_animal(self):
        self.genome = genome.Genome(self)
        self.phenotype = phenotype.Phenotype(self)
        self.drive_system = drive_system.DriveSystem(self)
        self.init_appearance()
        self.action_system = action_system.ActionSystem(self)
        self.nervous_system = nervous_system.NervousSystem(self)
        self.init_attack_strength()

    ############################################################################################################
    def init_attack_strength(self):
        m = config.Animal.teeth_attack_strength[1] - config.Animal.teeth_attack_strength[0]
        self.attack_strength = m * self.phenotype.trait_value_dict['Sharp Teeth'] + config.Animal.teeth_attack_strength[
            0]

    ############################################################################################################
    def init_appearance(self):

        self.visible_feature_label_list = ['Current Size', 'Age', 'Pregnant',
                                           'Facing N', 'Facing E', 'Facing S', 'Facing W',
                                           'Health', 'Energy', 'Arousal']
        self.num_visible_features = 0
        self.visible_feature_label_index_dict = {}

        appearance_list = []
        for i in range(len(self.visible_feature_label_list)):
            appearance_list.append(0)
            self.visible_feature_label_index_dict[self.visible_feature_label_list[i]] = self.num_visible_features
            self.num_visible_features += 1

        for label in self.genome.gene_dict:

            gene = self.genome.gene_dict[label]

            if gene.visible:
                self.visible_feature_label_list.append(gene.label)
                self.visible_feature_label_index_dict[gene.label] = self.num_visible_features
                self.num_visible_features += 1

                self.visible_feature_label_list.append(gene.label)
                trait_value = self.phenotype.trait_value_dict[gene.label]
                if gene.gene_type == 'float':
                    scaled_value = trait_value
                elif gene.gene_type == 'int':
                    scaled_value = trait_value / 10**gene.size
                    if scaled_value > 1:
                        scaled_value = 1
                else:
                    scaled_value = gene.sequence.mean()

                appearance_list.append(scaled_value)

        while len(appearance_list) < 30:
            appearance_list.append(0)
        if len(appearance_list) > 30:
            appearance_list = appearance_list[:30]

        self.appearance = np.array(appearance_list)
        self.update_appearance()

    ############################################################################################################
    def update_appearance(self):

        size = self.current_size/(10**self.genome.gene_dict['Max Size'].size)
        self.appearance[self.visible_feature_label_index_dict['Current Size']] = size

        age = self.age / 1000
        if age > 1:
            age = 1
        self.appearance[self.visible_feature_label_index_dict['Age']] = age

        pregnant = self.pregnant / config.Animal.gestation_rate
        if pregnant > 1:
            pregnant = 1
        self.appearance[self.visible_feature_label_index_dict['Pregnant']] = pregnant

        if self.orientation == 0:
            self.appearance[self.visible_feature_label_index_dict['Facing E']] = 1
        else:
            self.appearance[self.visible_feature_label_index_dict['Facing E']] = 0

        if self.orientation == 90:
            self.appearance[self.visible_feature_label_index_dict['Facing S']] = 1
        else:
            self.appearance[self.visible_feature_label_index_dict['Facing S']] = 0

        if self.orientation == 180:
            self.appearance[self.visible_feature_label_index_dict['Facing W']] = 1
        else:
            self.appearance[self.visible_feature_label_index_dict['Facing W']] = 0

        if self.orientation == 270:
            self.appearance[self.visible_feature_label_index_dict['Facing N']] = 1
        else:
            self.appearance[self.visible_feature_label_index_dict['Facing N']] = 0

        for i in range(self.drive_system.num_drives):
            drive = self.drive_system.drive_list[i]
            value = self.drive_system.drive_value_array[i]
            self.appearance[self.visible_feature_label_index_dict[drive]] = value

    ############################################################################################################
    def take_turn(self):

        start_time = time.time()
        self.nervous_system.stored_neural_feedforward()
        self.the_world.world_timers_array[2] += time.time() - start_time

        start_time = time.time()
        self.action_system.action_turn()
        self.the_world.world_timers_array[3] += time.time() - start_time

        start_time = time.time()
        self.drive_system.update_drives(self.action_system.action_choice)
        self.the_world.world_timers_array[4] += time.time() - start_time

        start_time = time.time()
        self.nervous_system.update_sensory_state()
        self.the_world.world_timers_array[5] += time.time() - start_time

        start_time = time.time()
        self.nervous_system.update_neural_weights()
        self.the_world.world_timers_array[6] += time.time() - start_time

        start_time = time.time()
        self.grow_older()
        self.the_world.world_timers_array[7] += time.time() - start_time

        start_time = time.time()
        self.update_appearance()
        self.the_world.world_timers_array[8] += time.time() - start_time

    ############################################################################################################
    def grow_older(self):
        self.age += 1

        if self.current_size < self.phenotype.trait_value_dict['Max Size']:
            self.current_size += 1 / config.Animal.childhood_length
            if self.current_size > self.phenotype.trait_value_dict['Max Size']:
                self.current_size = self.phenotype.trait_value_dict['Max Size']

    ############################################################################################################
    def get_pregnant(self, father_genome):
        self.pregnant = 1
        self.baby_daddy_genome = father_genome
        self.metabolism = config.Animal.metabolism * config.Animal.pregnant_metabolism_multiplier

    ############################################################################################################
    def bear_child(self):
        self.fetus.current_size = 0.1
        self.fetus.age = 0
        self.pregnant = 0
        self.fetus = None
        self.metabolism = config.Animal.metabolism

    ############################################################################################################
    def save_game(self):
        pass



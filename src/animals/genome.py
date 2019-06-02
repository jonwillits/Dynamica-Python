import random
from src import config
import numpy as np
import sys


class Genome:
    ############################################################################################################
    def __init__(self, animal, mother_genome=None, father_genome=None):
        self.animal = animal
        self.num_genes = None
        self.gene_dict = None
        self.gene_label_list = None
        self.gene_label_index_dict = None

        if mother_genome and father_genome:
            self.inherit_genome(mother_genome, father_genome)
        else:
            self.create_genome()

    ############################################################################################################
    def __repr__(self):
        output_string = "Genome: {} Genes\n".format(self.num_genes)
        for i in range(self.num_genes):
            label = self.gene_label_list[i]
            if self.gene_dict[label].specified_value is not None:
                mean = self.gene_dict[label].specified_value[0]
                stdev = self.gene_dict[label].specified_value[0]
            else:
                mean = None
                stdev = None

            output_string += '    {:3s}  {:24s}  {:6s}  {:2s} '.format(str(i),
                                                                       label,
                                                                       self.gene_dict[label].gene_type,
                                                                       str(self.gene_dict[label].size))

            output_string += 'Mutable:{:5s}  Visible:{:5s}  ({:5s},{:5s}) {}\n'.format(str(self.gene_dict[label].mutable),
                                                                                       str(self.gene_dict[label].visible),
                                                                                       str(mean),
                                                                                       str(stdev),
                                                                                       self.gene_dict[label].sequence)

        return output_string

    ############################################################################################################
    def inherit_genome(self, mother_genome, father_genome):

        self.num_genes = 0
        self.gene_dict = {}
        self.gene_label_list = []
        self.gene_label_index_dict = {}

        for i in range(self.num_genes):
            label = mother_genome.label_list[i]
            mother_sequence = mother_genome.gene_dict[label].sequence
            father_sequence = father_genome.gene_dict[label].sequence
            mutable = mother_genome.gene_dict[label].mutable
            visible = mother_genome.gene_dict[label].visible
            gene_type = mother_genome.gene_dict[label].gene_type
            size = len(mother_sequence)

            child_sequence = []
            for j in range(size):
                mother_nucleotide = mother_sequence[j]
                father_nucleotide = father_sequence[j]
                child_nucleotide = random.choice([mother_nucleotide, father_nucleotide])

                if mutable:
                    if random.uniform(0, 1) < config.Animal.mutation_rate:
                        if child_nucleotide == 0:
                            child_nucleotide = 1
                        else:
                            child_nucleotide = 0

                child_sequence[j] = child_nucleotide
            child_gene = Gene(label, gene_type, size, child_sequence, mutable, visible)

            self.gene_label_list.append(label)
            self.gene_dict[label] = child_gene
            self.gene_label_index_dict[label] = self.num_genes
            self.num_genes += 1

    ############################################################################################################
    def create_genome(self):

        self.num_genes = 0
        self.gene_dict = {}
        self.gene_label_list = []
        self.gene_label_index_dict = {}
        for label in self.animal.trait_init_dict:

            size = self.animal.trait_init_dict[label][0]
            gene_type = self.animal.trait_init_dict[label][1]
            trait_value = self.animal.trait_init_dict[label][2]
            mutable = self.animal.trait_init_dict[label][3]
            visible = self.animal.trait_init_dict[label][4]

            if trait_value is None:
                sequence = self.create_random_sequence(size, gene_type)
            else:
                if gene_type == 'vector':
                    sequence = self.create_specified_vector_sequence(label, trait_value[0], trait_value[1], size)
                elif gene_type == 'int':
                    sequence = self.create_specified_int_sequence(label, trait_value[0], trait_value[1], size)
                elif gene_type == 'float':
                    sequence = self.create_specified_float_sequence(label, trait_value[0], trait_value[1], size)
                else:
                    print("ERROR: trait init dict {} unrecognized gene type".format(label))
                    sys.exit(2)

            new_gene = Gene(label, gene_type, size, sequence, mutable, visible, trait_value)
            self.gene_label_list.append(label)
            self.gene_dict[label] = new_gene
            self.gene_label_index_dict[label] = self.num_genes
            self.num_genes += 1

    ############################################################################################################
    @staticmethod
    def create_random_sequence(size, gene_type):
        if gene_type == 'vector':
            sequence = np.zeros([size], int)
            for i in range(size):
                sequence[i] = random.choice([0, 1])
        elif gene_type == 'int' or gene_type == 'float':
            if size == 0:
                sequence = np.array([random.choice([0, 1])])
            else:
                sequence_list = []
                for i in range(size):
                    for j in range(9):
                        sequence_list.append(random.choice([0, 1]))
                sequence = np.array(sequence_list)
        else:
            print("ERROR: trait init dict unrecognized gene type {}".format(gene_type))
            sys.exit()

        return sequence

    ############################################################################################################
    @staticmethod
    def create_specified_vector_sequence(label, trait_value, trait_variability, size):
        if len(trait_value) != size:
            print("ERROR: trait init dict {} size mismatch".format(label))
            sys.exit()
        else:
            sequence = np.zeros([size], int)
            for i in range(size):
                sequence[i] = trait_value[i]
                if trait_variability is not None:
                    if random.random() < trait_variability:
                        if sequence[i] == 0:
                            sequence[i] = 1
                        elif sequence[i] == 1:
                            sequence[i] = 0
                        else:
                            print("ERROR: trait init dict {} vector gene has non-binary value".format(label))
                            sys.exit()

        for i in range(len(sequence)):
            if random.random() < trait_variability:
                if sequence[i] == 0:
                    sequence[i] = 1
                else:
                    sequence[i] = 0

        return np.array(sequence, int)

    ############################################################################################################
    @staticmethod
    def create_specified_int_sequence(label, trait_value, trait_variability, size):
        if not isinstance(trait_value, int):
            print("ERROR: trait {} value should match trait type (int)".format(label))
            sys.exit(2)

        if not trait_value >= 1:
            print("ERROR: trait {} int value should be >= 1".format(label))
            sys.exit(2)

        if len(str(trait_value)) > size:
            print("ERROR: trait init dict {} size mismatch".format(label))
            sys.exit()

        if trait_variability:
            value = round(random.normalvariate(trait_value, trait_variability))
            if value < 1:
                value = 1
            elif value > 10**size:
                value = 10**size
        else:
            value = trait_value
        string_value = str(value)

        if len(string_value) < size:
            while len(string_value) < size:
                string_value = "0" + string_value

        sequence = []
        for i in range(len(string_value)):
            string_digit = string_value[i]

            int_digit = int(string_digit)
            remainder = 9 - int_digit

            for j in range(int_digit):
                sequence.append(1)
            for j in range(remainder):
                sequence.append(0)

        return np.array(sequence, int)

    ############################################################################################################
    @staticmethod
    def create_specified_float_sequence(label, trait_value, trait_variability, size):
        if not isinstance(trait_value, float):
            print("ERROR: trait {} value should match trait type (float)".format(label))
            sys.exit(2)

        if not 0 <= trait_value <= 1.0:
            print("ERROR: trait {} value should be between 0.0 and 1.0".format(label))
            sys.exit(2)

        string_value = str(trait_value)[2:]
        if len(string_value) > size:
            print("ERROR: trait init dict {} size mismatch".format(label))
            sys.exit(2)

        if trait_variability:
            value = random.normalvariate(trait_value, trait_variability)
            if value < 0.0:
                value = 0.0
            elif value > 1.0:
                value = 1.0
            value = round(value, size)
        else:
            value = trait_value

        if value == 1.0:
            sequence = np.ones([9*size], int)
            return sequence

        else:
            string_value = str(value)[2:]

            if len(string_value) < size:
                while len(string_value) < size:
                    string_value = string_value + "0"

            sequence = []
            for i in range(len(string_value)):
                string_digit = string_value[i]

                int_digit = int(string_digit)
                remainder = 9 - int_digit
                for j in range(int_digit):
                    sequence.append(1)
                for j in range(remainder):
                    sequence.append(0)

            return np.array(sequence, int)


############################################################################################################
class Gene:
    ############################################################################################################
    def __init__(self, label, gene_type, size, sequence, mutable, visible, specified_value):

        self.label = label
        self.gene_type = gene_type
        self.size = size
        self.sequence = sequence
        if mutable == 'mutable':
            self.mutable = True
        else:
            self.mutable = False
        if visible == 'visible':
            self.visible = True
        else:
            self.visible = False

        self.specified_value = specified_value

    ############################################################################################################
    def __repr__(self):

        output_string = "{} {} {} {} {} {}".format(self.label, self.gene_type, self.size, self.mutable, self.visible,
                                                   self.sequence)
        return output_string

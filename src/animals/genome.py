import random
from src import config
import numpy as np


class Genome:
    ############################################################################################################
    def __init__(self, animal, mother_genome=None, father_genome=None):
        self.animal = animal
        self.num_genes = None
        self.num_nucleotides = None
        self.gene_list = None
        self.gene_label_list = None
        self.gene_index_dict = None

        if mother_genome and father_genome:
            self.inherit_genome(mother_genome, father_genome)
        else:
            self.create_genome()

    ############################################################################################################
    def __repr__(self):
        output_string = "Genome: {} Genes - {} Nucleotides\n".format(self.num_genes, self.num_nucleotides)
        for i in range(self.num_genes):
            output_string += '    {} {:24s}: {}\n'.format(self.gene_index_dict[self.gene_label_list[i]],
                                                      self.gene_label_list[i],
                                                      self.gene_list[i])

        return output_string

    ############################################################################################################
    def inherit_genome(self, mother_genome, father_genome):

        self.num_nucleotides = mother_genome.num_nucleotides
        self.num_genes = mother_genome.num_genes
        self.gene_list = []
        self.gene_label_list = []
        self.gene_index_dict = {}

        for i in range(self.num_genes):
            child_gene = []
            for j in range(len(mother_genome.gene_list[i])):
                mother_nucleotide = mother_genome.gene_list[i][j]
                father_nucleotide = father_genome.gene_list[i][j]
                child_nucleotide = random.choice([mother_nucleotide, father_nucleotide])
                if random.uniform(0, 1) < config.Animal.mutation_rate:
                    if child_nucleotide == 0:
                        child_nucleotide = 1
                    else:
                        child_nucleotide = 0
                child_gene.append(child_nucleotide)
            self.gene_list.append(np.array(child_gene, int))
            self.gene_label_list.append(mother_genome.gene_label_list[i])
            self.gene_index_dict[mother_genome.gene_label_list[i]] = i

    ############################################################################################################
    def create_genome(self):

        self.num_genes = 0
        self.num_nucleotides = 0
        self.gene_list = []
        self.gene_label_list = []
        self.gene_index_dict = {}

        for trait in config.Animal.trait_gene_size_dict:
            new_gene = []
            trait_info = config.Animal.trait_gene_size_dict[trait]

            for i in range(trait_info[0]):
                new_gene.append(random.choice([0, 1]))
                self.num_nucleotides += 1
            self.gene_list.append(np.array(new_gene, int))
            self.gene_label_list.append(trait)
            self.gene_index_dict[trait] = self.num_genes
            self.num_genes += 1

    ############################################################################################################
    def print_genome(self):
        print(self, end='')
        for i in range(self.num_genes):
            print("     ", self.gene_label_list[i], len(self.gene_list[i]), self.gene_list[i])

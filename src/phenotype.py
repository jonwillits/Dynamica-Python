from src import config
import numpy as np


############################################################################################################
class Phenotype:

    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal
        self.trait_gene_size_dict = config.Animal.trait_gene_size_dict

        self.num_traits = None
        self.trait_list = None
        self.trait_index_dict = None
        self.trait_value_dict = None

        self.init_traits()

    ############################################################################################################
    def __repr__(self):
        output_string =  "Phenotype: {} Traits\n".format(self.num_traits)
        for trait in self.trait_value_dict:
            output_string += "    {:16s}: {:0.3f}\n".format(trait, self.trait_value_dict[trait])
        return output_string

    ############################################################################################################
    def init_traits(self):

        self.num_traits = 0
        self.trait_list = []
        self.trait_index_dict = {}
        self.trait_value_dict = {}

        for trait in self.trait_gene_size_dict:

            self.trait_list.append(trait)
            self.trait_index_dict[trait] = self.num_traits
            self.num_traits += 1

            gene = self.animal.genome.gene_list[self.animal.genome.gene_index_dict[trait]]
            if self.trait_gene_size_dict[trait][1] == 'sum':
                self.trait_value_dict[trait] = gene.sum()

            elif self.trait_gene_size_dict[trait][1] == 'mean':
                self.trait_value_dict[trait] = round(gene.mean(), 6)

            elif self.trait_gene_size_dict[trait][1] == 'binary':
                self.trait_value_dict[trait] = int(np.array2string(gene, separator="")[1:-1], 2)

            elif self.trait_gene_size_dict[trait][1] == 'inv_binary':
                self.trait_value_dict[trait] = round(1 / (int(np.array2string(gene, separator="")[1:-1], 2) + 1), 6)

            elif self.trait_gene_size_dict[trait][1] == 'direction':
                if gene.sum() > 0:
                    self.trait_value_dict[trait] = 1
                else:
                    self.trait_value_dict[trait] = -1

            elif self.trait_gene_size_dict[trait][1] == 'vector':
                self.trait_value_dict[trait] = gene

    # ############################################################################################################
    # def update_appearance(self, appearance=None):
    #     self.appearance = appearance
    #     gene_location = self.genome_size - config.World.appearance_size
    #     for i in range(len(self.appearance)):
    #         if random.random() < config.Animal.within_sex_variance:
    #             if self.appearance[i] == 0:
    #                 self.appearance[i] = 1
    #             else:
    #                 self.appearance[i] = 0
    #         if self.appearance[i] == 0:
    #             self.genome[gene_location + i] = random.choice(["AC", "CA"])
    #         else:
    #             self.genome[gene_location + i] = random.choice(["GT", "TG"])
    #     self.appearance[0] = self.current_size / 5
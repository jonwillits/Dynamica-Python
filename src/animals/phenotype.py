import numpy as np


class Phenotype:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal

        self.num_traits = None
        self.trait_list = None
        self.trait_index_dict = None
        self.trait_value_dict = None

        self.init_traits()

    ############################################################################################################
    def __repr__(self):
        output_string = "Phenotype: {} Traits\n".format(self.num_traits)
        for trait in self.trait_value_dict:
            print(trait, self.trait_value_dict[trait])
            if isinstance(self.trait_value_dict[trait], np.ndarray):
                value = ""
                for e in self.trait_value_dict[trait]:
                    print(e.dtype)
                    if e.dtype == 'int64':
                        value += "{:0.0f} ".format(e)
                    else:
                        value += "{:0.2f} ".format(e)
                value = value[:-1]
            elif isinstance(self.trait_value_dict[trait], float):
                value = "{:0.3f}".format(self.trait_value_dict[trait])
            else:
                value = self.trait_value_dict[trait]
            output_string += "    {:24s}: {}\n".format(trait, str(value))
        return output_string

    ############################################################################################################
    def init_traits(self):

        self.num_traits = 0
        self.trait_list = []
        self.trait_index_dict = {}
        self.trait_value_dict = {}

        for i in range(self.animal.genome.num_genes):
            label = self.animal.genome.gene_label_list[i]
            self.trait_list.append(label)
            self.trait_index_dict[label] = self.num_traits
            self.num_traits += 1

            gene = self.animal.genome.gene_dict[label]

            if gene.gene_type == 'vector':
                self.trait_value_dict[label] = gene.sequence

            elif gene.gene_type == 'int':

                if gene.size == 0:
                    self.trait_value_dict[label] = gene.sequence[0]
                else:
                    sequence_matrix = gene.sequence.reshape(gene.size, 9)
                    final_value = 0
                    for j in range(gene.size):
                        current_sequence = sequence_matrix[gene.size-1-j, :]
                        value = current_sequence.sum()
                        final_value += value * 10**j
                    self.trait_value_dict[label] = final_value

            elif gene.gene_type == 'float':
                if gene.sequence.sum() == len(gene.sequence):
                    self.trait_value_dict[label] = 1.0
                else:
                    sequence_matrix = gene.sequence.reshape(gene.size, 9)
                    final_value = 0
                    for j in range(gene.size):
                        current_sequence = sequence_matrix[j, :]
                        value = current_sequence.sum()
                        final_value += value * 10**(-j-1)
                    self.trait_value_dict[label] = final_value




import tkinter as tk
import numpy as np


class PhenotypeWindow:

    def __init__(self, phenotype_window, animal):

        def on_configure(event):
            # update the scrollregion when everything is placed in the canvas
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.root = phenotype_window
        self.root.resizable(0, 0)
        self.animal = animal
        self.root.title("{} {} Genotype & Phenotype".format(self.animal.species, self.animal.id_number))

        biggest = self.get_biggest()
        print(biggest)
        self.width = biggest*5 + 50
        self.height = 800

        # create the canvas and scrollbar
        self.canvas = tk.Canvas(self.root, height=self.height, width=self.width)
        self.canvas.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.LEFT, fill='y')

        # call the configure function
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', on_configure)

        # put frame in canvas
        self.frame = tk.Frame(self.canvas, height=self.height, width=self.width)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # add content to frame
        for i in range(self.animal.phenotype.num_traits):
            name = self.animal.genome.gene_label_list[i]
            mutable = self.animal.genome.gene_dict[name].mutable
            visible = self.animal.genome.gene_dict[name].visible
            trait_value = self.animal.phenotype.trait_value_dict[name]
            gene_size = self.animal.genome.gene_dict[name].size
            sequence = self.animal.genome.gene_dict[name].sequence

            trait_string = "Trait Name: {}".format(name)
            self.name_value_label = tk.Label(self.frame, text=trait_string,
                                             font="Verdana 11 bold", anchor=tk.NW,
                                             justify=tk.LEFT, width=self.width, bd=0, padx=10, pady=0)
            self.name_value_label.pack(fill=tk.X)

            trait_string = "Trait Value: {}    Mutable: {}     Visible: {}".format(round(trait_value, 5),
                                                                                     mutable, visible)
            self.name_value_label = tk.Label(self.frame, text=trait_string,
                                             font="Verdana 11", anchor=tk.NW,
                                             justify=tk.LEFT, width=self.width, bd=0, padx=10, pady=0)
            self.name_value_label.pack(fill=tk.X)

            if gene_size > 0:
                sequence_matrix = sequence.reshape(gene_size, 9)
                sequence_string = ""
                for j in range(sequence_matrix.shape[0]):
                    sequence_string += np.array2string(sequence_matrix[j, :]) + " "
            else:
                sequence_string = np.array2string(sequence)

            self.gene_sequence_label = tk.Label(self.frame, text=sequence_string+"\n",
                                                font="Verdana 11", anchor=tk.W,
                                                justify=tk.LEFT, width=self.width, bd=0, padx=10, pady=0)
            self.gene_sequence_label.pack(fill=tk.X)

    def get_biggest(self):
        biggest = 0
        for i in range(self.animal.phenotype.num_traits):
            name = self.animal.genome.gene_label_list[i]
            new_len = len(name)
            if new_len > biggest:
                biggest = new_len
            trait_value = self.animal.phenotype.trait_value_dict[name]
            new_len = len("Trait Value: {}    Mutable: False     Visible: False\n".format(round(trait_value, 5)))
            if new_len > biggest:
                biggest = new_len
            gene_size = self.animal.genome.gene_dict[name].size
            sequence = self.animal.genome.gene_dict[name].sequence
            if gene_size > 0:
                sequence_matrix = sequence.reshape(gene_size, 9)
                sequence_string = ""
                for j in range(sequence_matrix.shape[0]):
                    sequence_string += np.array2string(sequence_matrix[j, :]) + " "
                new_len = len(sequence_string)
                if new_len > biggest:
                    biggest = new_len
        return biggest


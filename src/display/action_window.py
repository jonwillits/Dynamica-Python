import tkinter as tk
import numpy as np


class ActionWindow:
    ############################################################################################################
    def __init__(self, action_window, animal):

        def on_configure(event):
            # update the scrollregion when everything is placed in the canvas
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.root = action_window
        self.root.resizable(0, 0)
        self.a = animal
        self.root.title("{} {} Action System & History".format(self.a.species, self.a.id_number))

        self.width = 600
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

        self.action_system_title_label = None
        self.header_label = None
        self.animal_text_label = None

        self.action_history_title_label = None

        self.show_action_system_info()
        self.show_action_history()

    ############################################################################################################
    def show_action_system_info(self):

        self.action_system_title_label = tk.Label(self.frame, text="Action System Activation",
                                                  font="Courier 14 bold", anchor=tk.W, padx=30, pady=20)
        self.action_system_title_label.pack(fill=tk.X)

        input_state, hidden_state, output_state = self.a.nervous_system.neural_feedforward()
        action_outputs = output_state[self.a.nervous_system.a_indexes[0]:self.a.nervous_system.a_indexes[1] + 1]
        self.a.action_system.get_legal_action_probabilities(action_outputs)
        label_string = "Action Info    Activation    Probability"
        self.header_label = tk.Label(self.frame, text=label_string, font="Courier 11 bold", anchor=tk.W, padx=50)
        self.header_label.pack(fill=tk.X)
        for j in range(self.a.action_system.num_actions):
            label_string = "{:12s}  {:6.3f}        {:6.3f}".format(self.a.action_system.action_list[j] + ':',
                                                             action_outputs[j],
                                                             self.a.action_system.legal_action_prob_distribution[j])
            self.animal_text_label = tk.Label(self.frame, text=label_string, font="Courier 11", anchor=tk.W,
                                              padx=50)
            self.animal_text_label.pack(fill=tk.X)

    ############################################################################################################
    def show_action_history(self):
        self.action_history_title_label = tk.Label(self.frame, text="Action System History",
                                                   font="Courier 14 bold", anchor=tk.SW, padx=30, height=2)
        self.action_history_title_label.pack(fill=tk.X)

        for i in range(len(self.a.action_system.action_history_list)):
            self.action_history_label = tk.Label(self.frame,
                                                 text=self.a.action_system.action_history_list[-(i+1)],
                                                 font="Courier 11", anchor=tk.NW, padx=50, justify=tk.LEFT)
            self.action_history_label.pack(fill=tk.X)


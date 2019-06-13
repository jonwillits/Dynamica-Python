import tkinter as tk
import numpy as np
from src.display import plot_species_info


class SpeciesInfoWindow:
    ############################################################################################################
    def __init__(self, display, master, the_world, species, image_dict):
        self.master = master
        self.master.title("Dynamica: {} Information".format(species))
        self.window_height = 1200
        self.window_width = 1000
        self.the_world = the_world
        self.species = species
        self.image_dict = image_dict
        self.display = display

        self.info_canvas = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.info_canvas.pack()

        self.summary_frame = None
        self.species_header = None
        self.trait_header = None
        self.action_header = None
        self.drive_header = None
        self.error_header = None

        self.column_labels1 = None
        self.column_labels2 = None
        self.column_labels3 = None
        self.column_labels4 = None
        self.column_labels5 = None

        self.summary_label_list = []

        self.refresh()

    ############################################################################################################
    def refresh(self):
        data_matrix = self.the_world.animal_summary_dict[self.species][1]

        # create the summary frame
        self.summary_frame = tk.Frame(self.info_canvas, width=1000, height=1200)
        self.summary_frame.grid(row=0, column=0)

        # create the Species Label at the top
        self.species_header = tk.Label(self.summary_frame,
                                       text="{} Information".format(self.species),
                                       font="Verdana 16 bold", )
        self.species_header.place(x=10, y=10)

        # create the N, age, size summary info
        self.column_labels1 = tk.Label(self.summary_frame,
                                       text="Start       Now  Change", font="Verdana 12 bold", anchor=tk.W)
        self.column_labels1.place(x=220, y=53)

        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Pop Size:", data_matrix, 1, 20, 70)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Age:", data_matrix, 2, 20, 90)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Size:", data_matrix, 3, 20, 110)
        self.summary_label_list.append(summary_label)

        # create the phenotype summary info
        self.trait_header = tk.Label(self.summary_frame, text="Phenotypic traits", font="Verdana 14 bold", )
        self.trait_header.place(x=10, y=150)
        self.column_labels2 = tk.Label(self.summary_frame,
                                       text="Start      Now        Change", font="Verdana 12 bold", anchor=tk.W)
        self.column_labels2.place(x=220, y=153)
        i = 4
        j = 0
        for trait in self.the_world.animal_list[0].phenotype.trait_list:
            y = 170 + (20*(i-4))
            summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                         trait+":", data_matrix, i, 20, y)
            self.summary_label_list.append(summary_label)
            i += 1
            j += 1

        # create the drive summary info
        self.drive_header = tk.Label(self.summary_frame, text="Drive States", font="Verdana 14 bold", )
        self.drive_header.place(x=500, y=150)
        self.column_labels3 = tk.Label(self.summary_frame,
                                       text="Start      Now        Change", font="Verdana 12 bold", anchor=tk.W)
        self.column_labels3.place(x=720, y=153)
        k = 0
        for drive in self.the_world.animal_list[0].drive_system.drive_list:
            y = 170 + (20*(i-4-j))
            summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                         drive+":", data_matrix, i, 510, y)
            self.summary_label_list.append(summary_label)
            i += 1
            k += 1

        # create the action summary info
        self.action_header = tk.Label(self.summary_frame, text="Action Activations", font="Verdana 14 bold", )
        self.action_header.place(x=500, y=250)
        self.column_labels4 = tk.Label(self.summary_frame,
                                       text="Start      Now        Change", font="Verdana 12 bold", anchor=tk.W)
        self.column_labels4.place(x=720, y=253)
        m = 0
        for action in self.the_world.animal_list[0].action_system.action_list:
            y = 270 + (20 * (i - 4 - j - k))
            summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                         action+":", data_matrix, i, 510, y)
            self.summary_label_list.append(summary_label)
            i += 1
            m += 1

        # create the error summary info
        self.error_header = tk.Label(self.display, self.summary_frame, text="Neural Network Error",
                                     font="Verdana 14 bold")
        self.error_header.place(x=500, y=410)
        self.column_labels4 = tk.Label(self.summary_frame,
                                       text="Start      Now        Change", font="Verdana 12 bold", anchor=tk.W)
        self.column_labels4.place(x=720, y=413)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Prediction Error:", data_matrix, i, 510, 430)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Health Reinforcement:", data_matrix, i+1, 510, 450)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "HealthΔ Reinforcement:", data_matrix, i+2, 510, 470)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Energy Reinforcement:", data_matrix, i+3, 510, 490)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "EnergyΔ Reinforcement:", data_matrix, i+4, 510, 510)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "Arousal Reinforcement:", data_matrix, i+5, 510, 530)
        self.summary_label_list.append(summary_label)
        summary_label = SummaryLabel(self.display, self.summary_frame, self.species, self.image_dict,
                                     "ArousalΔ Reinforcement:", data_matrix, i+6, 510, 550)
        self.summary_label_list.append(summary_label)


############################################################################################################
class SummaryLabel:

    def __init__(self, display, summary_frame, species, image_dict, label_text, data_matrix, column, x, y):
        self.display = display
        self.summary_frame = summary_frame
        self.label_text = label_text

        if len(data_matrix.shape) == 1:
            self.val1 = str(round(data_matrix[column], 3))
            self.val2 = self.val1
            self.val3 = "0"
            self.data_vector = np.array(data_matrix[column])
        else:
            self.val1 = str(round(data_matrix[0, column], 3))
            self.val2 = str(round(data_matrix[-1, column], 3))
            self.val3 = str(round(data_matrix[-1, column] - data_matrix[0, column], 3))
            self.data_vector = data_matrix[:, column]

        self.x = x
        self.y = y
        self.species = species

        click_image = image_dict['assets/images/blue_square.gif']
        self.click_icon = tk.Label(self.summary_frame, image=click_image, anchor=tk.W)
        self.click_icon.place(x=self.x-2, y=self.y+4)

        self.summary_title1 = tk.Label(self.summary_frame, text=self.label_text, font="Verdana 12 bold", anchor=tk.W)
        self.summary_title1.place(x=self.x + 10, y=self.y)

        self.summary_string = "   {:8s}     {:8s}      {:8s}".format(self.val1, self.val2, self.val3)
        self.summary_title2 = tk.Label(self.summary_frame, text=self.summary_string, font="Verdana 12", anchor=tk.W)
        self.summary_title2.place(x=self.x+200, y=self.y)

        plot_tuple = (species, label_text, self.data_vector)
        self.click_icon.bind('<Double-Button-1>',
                             lambda event, arg=plot_tuple: self.property_summary_on_double_click(event, arg))

    ############################################################################################################
    def property_summary_on_double_click(self, event, plot_tuple):
        print("Species Summary", plot_tuple, event)
        self.display.species_summary_window = tk.Toplevel(self.display.root)
        self.animal_plot_window_instance = plot_species_info.PlotSpeciesInfo(self.display.species_summary_window,
                                                                           plot_tuple,
                                                                           self.display)

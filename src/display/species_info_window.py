import tkinter as tk


class SpeciesInfoWindow:
    ############################################################################################################
    def __init__(self, master, the_world, species):
        self.master = master
        self.master.title("Dynamica: {} Information".format(species))
        self.window_height = 1200
        self.window_width = 500
        self.the_world = the_world
        self.species = species

        self.info_canvas = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.info_canvas.pack()

        self.summary_frame = None
        self.species_header = None
        self.summary_title = None
        self.summary_title1 = None
        self.summary_title2 = None

        self.refresh()

    ############################################################################################################
    def refresh(self):
        data_matrix = self.the_world.animal_summary_dict[self.species][1]

        if len(self.the_world.animal_summary_dict[self.species][1].shape) == 1:
            first = data_matrix
            last = data_matrix
        else:
            first = data_matrix[0, :]
            last = data_matrix[-1, :]

        self.summary_frame = tk.Frame(self.info_canvas, width=500, height=1200)
        self.summary_frame.grid(row=0, column=0)

        self.species_header = tk.Label(self.summary_frame,
                                       text="{} Information".format(self.species),
                                       font="Verdana 12 bold", )
        self.species_header.place(x=10, y=10)

        self.summary_title = tk.Label(self.summary_frame, text=" Start    Now", font="Verdana 12 bold", anchor=tk.W)
        self.summary_title.place(x=240, y=50)

        summary_string = "   {:>5s}     {:>5s}".format(str(first[1]), str(last[1]))
        self.summary_title1 = tk.Label(self.summary_frame, text="Population Size:", font="Verdana 12 bold", anchor=tk.W)
        self.summary_title2 = tk.Label(self.summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        self.summary_title1.place(x=20, y=70)
        self.summary_title2.place(x=240, y=70)

        summary_string = "   {:>5s}     {:>5s}".format(str(first[2]), str(last[2]))
        self.summary_title1 = tk.Label(self.summary_frame, text="Age:", font="Verdana 12 bold", anchor=tk.W)
        self.summary_title2 = tk.Label(self.summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        self.summary_title1.place(x=20, y=90)
        self.summary_title2.place(x=240, y=90)

        summary_string = "   {:>5s}     {:>5s}".format(str(first[3]), str(last[3]))
        self.summary_title1 = tk.Label(self.summary_frame, text="Size:", font="Verdana 12 bold", anchor=tk.W)
        self.summary_title2 = tk.Label(self.summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        self.summary_title1.place(x=20, y=110)
        self.summary_title2.place(x=240, y=110)

        i = 4
        for trait in self.the_world.animal_list[0].phenotype.trait_list:
            summary_string = "   {:0.2f}       {:0.2f}".format(first[i], last[i])
            self.summary_title1 = tk.Label(self.summary_frame, text=trait, font="Verdana 12 bold", anchor=tk.W)
            self.summary_title2 = tk.Label(self.summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
            self.summary_title1.place(x=20, y=150 + (20*(i-4)))
            self.summary_title2.place(x=240, y=150 + (20*(i-4)))
            i += 1



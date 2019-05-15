import tkinter as tk


class SpeciesInfoWindow:
    ############################################################################################################
    def __init__(self, master, the_world, species):
        self.master = master
        self.master.title("Dynamica: {} Information".format(species))
        self.window_height = 800
        self.window_width = 500
        self.the_world = the_world
        self.species = species

        self.info_canvas = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.info_canvas.pack()

        self.refresh()

    ############################################################################################################
    def refresh(self):

        s0 = self.the_world.initial_animal_summary_dict[self.species]
        if self.the_world.current_turn == 1:
            st = s0
        else:
            st = self.the_world.calc_species_summary(self.species)

        summary_frame = tk.Frame(self.info_canvas, width=500, height=800)
        summary_frame.grid(row=0, column=0)

        species_header = tk.Label(summary_frame, text="{} Information".format(self.species), font="Verdana 12 bold", )
        species_header.place(x=10, y=10)

        summary_title = tk.Label(summary_frame, text=" Start    Now", font="Verdana 12 bold", anchor=tk.W)
        summary_title.place(x=240, y=50)

        summary_string = "   {:>5s}     {:>5s}".format(str(s0['N']), str(st['N']))
        summary_title1 = tk.Label(summary_frame, text="Population Size:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=70)
        summary_title2.place(x=240, y=70)

        summary_string = "   {:5.1f}     {:5.1f}".format(s0['Age'], st['Age'])
        summary_title1 = tk.Label(summary_frame, text="Average Age:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=90)
        summary_title2.place(x=240, y=90)

        summary_string = "   {:0.2f}      {:0.2f}".format(s0['Sex'], st['Sex'])
        summary_title1 = tk.Label(summary_frame, text="Proportion Female:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=110)
        summary_title2.place(x=240, y=110)

        summary_string = "   {:0.2f}       {:0.2f}".format(s0['Size'], st['Size'])
        summary_title1 = tk.Label(summary_frame, text="Average Max Size:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=130)
        summary_title2.place(x=240, y=130)

        summary_string = "{:0.2f}    {:0.2f}".format(s0['Hidden Neurons'], st['Hidden Neurons'])
        summary_title1 = tk.Label(summary_frame, text="Average Hidden Neurons:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=160)
        summary_title2.place(x=240, y=160)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Prediction Learning Rate'], st['Prediction Learning Rate'])
        summary_title1 = tk.Label(summary_frame, text="Average Learning Rate:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=180)
        summary_title2.place(x=240, y=180)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Weight Init Stdev'], st['Weight Init Stdev'])
        summary_title1 = tk.Label(summary_frame, text="Weight Init Stdev:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=200)
        summary_title2.place(x=240, y=200)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Targets'][0],
                                                         st['Drive Targets'][0])
        summary_title1 = tk.Label(summary_frame, text="Health Target:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=230)
        summary_title2.place(x=240, y=230)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Reinforcement Rates'][0, 0],
                                                         st['Drive Reinforcement Rates'][0, 0])
        summary_title1 = tk.Label(summary_frame, text="Health Value LR:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=250)
        summary_title2.place(x=240, y=250)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Reinforcement Rates'][1, 0],
                                                         st['Drive Reinforcement Rates'][1, 0])
        summary_title1 = tk.Label(summary_frame, text="Health Change LR:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=270)
        summary_title2.place(x=240, y=270)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Targets'][1],
                                                         st['Drive Targets'][1])
        summary_title1 = tk.Label(summary_frame, text="Energy Target:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=290)
        summary_title2.place(x=240, y=290)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Reinforcement Rates'][0, 1],
                                                         st['Drive Reinforcement Rates'][0, 1])
        summary_title1 = tk.Label(summary_frame, text="Energy Value LR:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=310)
        summary_title2.place(x=240, y=310)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Reinforcement Rates'][1, 1],
                                                         st['Drive Reinforcement Rates'][1, 1])
        summary_title1 = tk.Label(summary_frame, text="Energy Change LR:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=330)
        summary_title2.place(x=240, y=330)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Targets'][2],
                                                         st['Drive Targets'][2])
        summary_title1 = tk.Label(summary_frame, text="Arousal Target:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=350)
        summary_title2.place(x=240, y=350)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Reinforcement Rates'][0, 2],
                                                         st['Drive Reinforcement Rates'][0, 2])
        summary_title1 = tk.Label(summary_frame, text="Arousal Value LR:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=370)
        summary_title2.place(x=240, y=370)

        summary_string = "  {:0.3f}      {:0.3f}".format(s0['Drive Reinforcement Rates'][1, 2],
                                                         st['Drive Reinforcement Rates'][1, 2])
        summary_title1 = tk.Label(summary_frame, text="Arousal Change LR:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=390)
        summary_title2.place(x=240, y=390)

        so_action_outputs = s0['Action Outputs']
        st_action_outputs = st['Action Outputs']
        so_action_probs = so_action_outputs / so_action_outputs.sum()
        st_action_probs = st_action_outputs / st_action_outputs.sum()

        summary_string = "  {:0.3f}      {:0.3f}".format(so_action_probs[0], st_action_probs[0])
        summary_title1 = tk.Label(summary_frame, text="Average Rest Probability:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=420)
        summary_title2.place(x=240, y=420)

        summary_string = "  {:0.3f}      {:0.3f}".format(so_action_probs[1], st_action_probs[1])
        summary_title1 = tk.Label(summary_frame, text="Average Attack Probability:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=440)
        summary_title2.place(x=240, y=440)

        summary_string = "  {:0.3f}      {:0.3f}".format(so_action_probs[2], st_action_probs[2])
        summary_title1 = tk.Label(summary_frame, text="Average Eat Probability:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=460)
        summary_title2.place(x=240, y=460)

        summary_string = "  {:0.3f}      {:0.3f}".format(so_action_probs[3], st_action_probs[3])
        summary_title1 = tk.Label(summary_frame, text="Average Procreate Probability:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=480)
        summary_title2.place(x=240, y=480)

        summary_string = "  {:0.3f}      {:0.3f}".format(so_action_probs[4], st_action_probs[4])
        summary_title1 = tk.Label(summary_frame, text="Average Turn Probability:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=500)
        summary_title2.place(x=240, y=500)

        summary_string = "  {:0.3f}      {:0.3f}".format(so_action_probs[5], st_action_probs[5])
        summary_title1 = tk.Label(summary_frame, text="Average Move Probability:", font="Verdana 12 bold", anchor=tk.W)
        summary_title2 = tk.Label(summary_frame, text=summary_string, font="Verdana 12", anchor=tk.W)
        summary_title1.place(x=20, y=520)
        summary_title2.place(x=240, y=520)
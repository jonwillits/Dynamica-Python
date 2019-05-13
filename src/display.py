import tkinter as tk
import os
import sys
from src import config


############################################################################################################
############################################################################################################
class Display:
    ############################################################################################################
    def __init__(self, the_world):
        self.the_world = the_world
        self.turn = 0
        self.image_dict = None
        self.running = False

        self.num_rows = config.World.num_rows
        self.num_columns = config.World.num_columns
        self.grid_size = config.World.grid_size
        self.world_height = None
        self.world_width = None

        self.root = None
        self.root_height = config.GlobalOptions.window_height
        self.root_width = config.GlobalOptions.window_width

        self.scroll_frame = None
        self.main_canvas = None
        self.main_canvas_height = self.root_height - 50
        self.main_canvas_width = self.root_width - 500 - 15
        self.wn = None

        self.summary_canvas = None
        self.summary_canvas_height = self.root_height - 35
        self.summary_canvas_width = 500

        self.species_summary_window = None

        self.info_window = None
        self.info_window_instance = None

        self.button_canvas = None
        self.button_canvas_height = 20
        self.button_canvas_width = self.root_width
        self.button_height = 2
        self.button_width = 8
        self.next_button = None
        self.run_button = None
        self.save_button = None
        self.quit_button = None

        self.configure_sizes()
        self.create_main_window()
        self.create_main_canvas()
        self.create_summary_canvas()

        self.create_buttons()

        self.load_images()
        self.draw_terrain()
        self.draw_objects()
        self.draw_animals()
        self.update_summary_display()

    ############################################################################################################
    def configure_sizes(self):
        self.world_height = self.num_rows * self.grid_size
        self.world_width = self.num_columns * self.grid_size

    ############################################################################################################
    def create_main_window(self):
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.title("Dynamica: Turn {}".format(self.turn))

    ############################################################################################################
    def create_main_canvas(self):

        self.scroll_frame = tk.Frame(self.root)
        self.scroll_frame.grid(row=0, column=0)

        def on_frame_configure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))

        self.main_canvas = tk.Canvas(self.scroll_frame,
                                     height=self.main_canvas_height, width=self.main_canvas_width,
                                     bd=0, highlightthickness=0,
                                     bg='#000000',
                                     scrollregion=(0, 0, self.main_canvas_width, self.main_canvas_height))

        game_frame = tk.Frame(self.main_canvas)
        game_frame.grid(row=0, column=0)

        vsb = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.main_canvas.yview)
        hsb = tk.Scrollbar(self.scroll_frame, orient="horizontal", command=self.main_canvas.xview)
        self.main_canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.grid(sticky=tk.N+tk.S+tk.E)
        hsb.grid(sticky=tk.E+tk.W+tk.S)
        self.main_canvas.grid(row=0, column=0)
        self.main_canvas.create_window((4, 4), window=game_frame, anchor="nw")

        game_frame.bind("<Configure>", lambda event, canvas=self.main_canvas: on_frame_configure(canvas))

        self.main_canvas.bind('<Double-Button-1>', self.main_canvas_on_double_click)

    ############################################################################################################
    def main_canvas_on_double_click(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        self.show_tile_click_info(x, y)

    ############################################################################################################
    def animal_summary_on_double_click(self, event):
        print("Species click event", event)
        species = 'Zebra'
        if self.species_summary_window is not None:
            self.species_summary_window.destroy()
        self.species_summary_window = tk.Toplevel(self.root)
        self.species_summary_window_instance = SpeciesInfoWindow(self.species_summary_window, self.the_world, species)

    ############################################################################################################
    def create_summary_canvas(self):
        self.summary_canvas = tk.Canvas(self.root,
                                        width=self.summary_canvas_width,
                                        height=self.summary_canvas_height,
                                        bg="grey", bd=0, highlightthickness=0)
        self.summary_canvas.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0)

    ############################################################################################################
    def create_buttons(self):
        self.button_canvas = tk.Canvas(self.root,
                                       width=self.button_canvas_width,
                                       height=self.button_canvas_height,
                                       bd=0, highlightthickness=0)
        self.button_canvas.grid(row=1, column=0, columnspan=2, padx=0, pady=0, ipadx=0, ipady=0)

        self.button_height = 2
        self.button_width = 8

        self.next_button = tk.Button(self.button_canvas, text="Next", fg="black",
                                     height=self.button_height, width=self.button_width,
                                     command=self.next_turn)
        self.next_button.grid(row=0, column=0, sticky=tk.W)

        self.run_button = tk.Button(self.button_canvas, text="Run", fg="black",
                                    height=self.button_height, width=self.button_width,
                                    command=self.run_game)
        self.run_button.grid(row=0, column=1, sticky=tk.W)

        self.save_button = tk.Button(self.button_canvas, text="Save", fg="black",
                                    height=self.button_height, width=self.button_width,
                                    command=self.save_game)
        self.save_button.grid(row=0, column=2, sticky=tk.W)

        self.quit_button = tk.Button(self.button_canvas, text="Quit", fg="black",
                                     height=self.button_height, width=self.button_width,
                                     command=self.quit_game)
        self.quit_button.grid(row=0, column=3, sticky=tk.E)

    ############################################################################################################
    def load_images(self):
        self.image_dict = {}
        ls = os.listdir('assets/images/')
        for filename in ls:
            if not filename == '.DS_Store':
                if filename[-3:] == 'gif':
                    path = 'assets/images/' + filename
                    new_image = tk.PhotoImage(file=path)
                    self.image_dict[path] = new_image

    ############################################################################################################
    def get_screen_coordinates(self, grid_x, grid_y):
        screen_x = grid_x * self.grid_size
        screen_y = grid_y * self.grid_size
        return screen_x, screen_y

    ############################################################################################################
    def get_grid_coordinates(self, screen_x, screen_y):
        grid_x = int(round((screen_x - self.grid_size/2) / self.grid_size))
        grid_y = int(round((screen_y - self.grid_size/2) / self.grid_size))
        return grid_x, grid_y

    ############################################################################################################
    def draw_terrain(self):
        for i in range(self.the_world.num_rows):
            for j in range(self.the_world.num_columns):
                current_tile = self.the_world.map[(j, i)]
                x, y = self.get_screen_coordinates(j, i)
                self.main_canvas.create_image(x, y, anchor=tk.NW, image=self.image_dict[current_tile.image])

    ############################################################################################################
    def update_summary_display(self):
        # create the summary display frame
        self.summary_frame = tk.Frame(self.summary_canvas,
                                 width=self.summary_canvas_width-20,
                                 height=self.summary_canvas_height-20,
                                 bd=0, highlightthickness=0,
                                 bg="white")
        self.summary_frame.place(x=10, y=10)

        # create the summary display main title
        summary_main_title = tk.Label(self.summary_frame, text="Dynamica Summary", font="Verdana 16 bold", anchor=tk.W)
        summary_main_title.place(x=10, y=10)

        # create the plants display

        # create the grass label
        summary_plant_title = tk.Label(self.summary_frame, text="Plants", font="Verdana 12 bold", anchor=tk.W)
        summary_plant_title.place(x=10, y=50)

        # get and place the grass image
        self.grass_image = tk.PhotoImage(file='assets/images/plains.gif')
        plant_image_label = tk.Label(self.summary_frame, image=self.grass_image, anchor=tk.W)
        plant_image_label.place(x=30, y=80)

        # get and place the grass data, or fill in zeros if no grass
        if 'Grass' in self.the_world.turn_summary_dict['Plant']:
            grass_data = self.the_world.turn_summary_dict['Plant']['Grass']
            plant_text_string = "Grass     Tiles: {}    Qty: {:3.2f}%".format(grass_data[0], 100 * (
                        grass_data[1] / (grass_data[0] * 100)))
        else:
            plant_text_string = "Grass     Tiles: 0    Qty: 0"
        plant_text_label = tk.Label(self.summary_frame, text=plant_text_string, font="Verdana 10", anchor=tk.W)
        plant_text_label.place(x=70, y=90)

        # create the animals display
        summary_title = tk.Label(self.summary_frame, text="Animals", font="Verdana 12 bold", anchor=tk.W)
        summary_title.place(x=10, y=150)

        # create the zebra display
        # get and place the zebra image
        self.zebra_image = tk.PhotoImage(file='assets/images/Zebra0.gif')
        zebra_image_label = tk.Label(self.summary_frame, image=self.zebra_image, anchor=tk.W)
        zebra_image_label.place(x=30, y=180)

        if 'Zebra' in self.the_world.turn_summary_dict['Animal']:
            zebra_data = self.the_world.turn_summary_dict['Animal']['Zebra']
            qty = str("{:0.0f}".format(zebra_data[0]))
            health = str("{:3.2f}".format(zebra_data[1]))
            energy = str("{:3.2f}".format(zebra_data[2]))
            arousal = str("{:3.2f}".format(zebra_data[3]))
            zebra_text_string = "Zebra   Qty: {:5s}   ".format(qty)
            zebra_text_string += "Health: {:<7s}    ".format(health)
            zebra_text_string += "Energy: {:<7s}    ".format(energy)
            zebra_text_string += "Arousal: {:<7s}    ".format(arousal)
        else:
            zebra_text_string = "Zebra   Qty: 0   Health: NA   Energy: NA    Arousal: NA"

        zebra_text_label = tk.Label(self.summary_frame, text=zebra_text_string, font="Verdana 10", anchor=tk.W)
        zebra_text_label.place(x=70, y=190)
        zebra_image_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)
        zebra_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)

        # create the lion display
        # get and place the zebra image
        self.lion_image = tk.PhotoImage(file='assets/images/Lion0.gif')
        lion_image_label = tk.Label(self.summary_frame, image=self.lion_image, anchor=tk.W)
        lion_image_label.place(x=30, y=220)

        if 'Lion' in self.the_world.turn_summary_dict['Animal']:
            lion_data = self.the_world.turn_summary_dict['Animal']['Lion']
            qty = str("{:0.0f}".format(lion_data[0]))
            health = str("{:3.2f}".format(lion_data[1]))
            energy = str("{:3.2f}".format(lion_data[2]))
            arousal = str("{:3.2f}".format(lion_data[3]))
            lion_text_string = "Lion   Qty: {:5s}   ".format(qty)
            lion_text_string += "Health: {:<7s}    ".format(health)
            lion_text_string += "Energy: {:<7s}    ".format(energy)
            lion_text_string += "Arousal: {:<7s}    ".format(arousal)
        else:
            lion_text_string = "Lion   Qty: 0   Health: NA   Energy: NA    Arousal: NA"

        lion_text_label = tk.Label(self.summary_frame, text=lion_text_string, font="Verdana 10", anchor=tk.W)
        lion_text_label.place(x=70, y=230)
        lion_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)
        lion_text_label.bind('<Double-Button-1>', self.animal_summary_on_double_click)

    ############################################################################################################
    def draw_animals(self):
        for animal in self.the_world.animal_list:
            x, y = self.get_screen_coordinates(animal.position[0], animal.position[1])
            image = animal.image_dict[animal.orientation]
            self.main_canvas.create_image(x+2, y+2, anchor=tk.NW, image=self.image_dict[image])

    ############################################################################################################
    def draw_objects(self):
        for world_object in self.the_world.object_list:
            x, y = self.get_screen_coordinates(world_object.position[0], world_object.position[1])
            image = world_object.graphic_object
            self.main_canvas.create_image(x+6, y+6, anchor=tk.NW, image=self.image_dict[image])

    ############################################################################################################
    def run_game(self):

        if self.running:
            self.running = False
            self.run_button.config(text="Run")
        else:
            self.running = True
            self.run_button.config(text="Pause")

        while self.running:
            self.next_turn()

    ############################################################################################################
    def next_turn(self):
        self.turn += 1
        try:
            self.root.title("Dynamica: Turn {}".format(self.turn))
        except:
            sys.exit(1)
        self.the_world.next_turn()

        self.main_canvas.delete("all")
        self.draw_terrain()
        self.draw_objects()
        self.draw_animals()
        self.update_summary_display()
        self.root.update()
        self.root.update_idletasks()

    ############################################################################################################
    def save_game(self):
        pass

    ############################################################################################################
    def quit_game(self):
        if self.running:
            self.run_game()
        sys.exit(1)

    ############################################################################################################
    def show_tile_click_info(self, x, y):
        grid_x, grid_y = self.get_grid_coordinates(x, y)
        if 0 <= grid_x <= self.num_columns - 1:
            if 0 <= grid_y <= self.num_rows - 1:
                if self.info_window is not None:
                    self.info_window.destroy()
                self.info_window = tk.Toplevel(self.root)
                self.info_window_instance = GridInfoWindow(self.info_window, self.the_world, (grid_x, grid_y))


############################################################################################################
############################################################################################################
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


############################################################################################################
############################################################################################################
class GridInfoWindow:
    ############################################################################################################
    def __init__(self, master, the_world, grid_location):
        self.master = master
        self.master.title("Dynamica: ({},{}) Information".format(grid_location[0], grid_location[1]))
        self.window_height = 800
        self.window_width = 400
        self.the_world = the_world

        self.terrain_image = None
        self.plant_image = None
        self.object_image = None
        self.animal_image = None

        self.info_canvas = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.info_canvas.pack()
        self.refresh(grid_location)

    ############################################################################################################
    def refresh(self, grid_location):

        self.get_terrain_info(grid_location)
        self.get_plant_info(grid_location)
        self.get_object_info(grid_location)
        self.get_animal_info(grid_location)

    ############################################################################################################
    def get_terrain_info(self, grid_location):
        terrain_frame = tk.Frame(self.info_canvas, width=400, height=100)
        terrain_frame.grid(row=0, column=0)

        terrain_header = tk.Label(terrain_frame, text="Terrain Information", font="Verdana 12 bold", )
        terrain_header.place(x=10, y=10)

        self.terrain_image = tk.PhotoImage(file=self.the_world.map[grid_location].image)
        terrain_image_label = tk.Label(terrain_frame, image=self.terrain_image, anchor=tk.W)
        terrain_image_label.place(x=30, y=30)

        terrain_text_label = tk.Label(terrain_frame, text=self.the_world.map[grid_location].terrain_type,
                                      font="Verdana 11", anchor=tk.W)
        terrain_text_label.place(x=70, y=40)

    ############################################################################################################
    def get_plant_info(self, grid_location):
        plant_frame = tk.Frame(self.info_canvas, width=400, height=100)
        plant_frame.grid(row=1, column=0)

        plant_header = tk.Label(plant_frame, text="Vegetation Information", font="Verdana 12 bold")
        plant_header.place(x=10, y=10)

        if len(self.the_world.map[grid_location].plant_list) == 0:
            plant_string = "None"
        else:
            plant = self.the_world.map[grid_location].plant_list[0]
            plant_string = "{}: {}".format(plant.species, plant.quantity)

        plant_info = tk.Label(plant_frame, text=plant_string, font="Verdana 11")
        plant_info.place(x=30, y=40)

    ############################################################################################################
    def get_object_info(self, grid_location):
        object_frame = tk.Frame(self.info_canvas, width=400, height=100)
        object_frame.grid(row=2, column=0)

        object_header = tk.Label(object_frame, text="Object Information", font="Verdana 12 bold")
        object_header.place(x=10, y=10)
        if len(self.the_world.map[grid_location].object_list) == 0:
            object_string = "None"
        else:
            world_object = self.the_world.map[grid_location].object_list[0]
            object_string = "{}: {}".format(world_object.object_type, world_object.quantity)

        object_info = tk.Label(object_frame, text=object_string, font="Verdana 11")
        object_info.place(x=30, y=40)

    ############################################################################################################
    def get_animal_info(self, grid_location):
        animal_frame = tk.Frame(self.info_canvas, width=400, height=500)
        animal_frame.grid(row=3, column=0)

        animal_header = tk.Label(animal_frame, text="Animal Information", font="Verdana 12 bold")
        animal_header.place(x=10, y=10)

        if len(self.the_world.map[grid_location].animal_list) == 0:
            animal_info = tk.Label(animal_frame, text="None", font="Verdana 11 bold")
            animal_info.place(x=30, y=30)
        else:
            animal = self.the_world.map[grid_location].animal_list[0]
            label_string = "{} {}".format(animal.species, animal.id_number)
            self.animal_image = tk.PhotoImage(file=animal.image_dict[0])
            animal_image_label = tk.Label(animal_frame, image=self.animal_image, anchor=tk.W)
            animal_image_label.place(x=30, y=30)
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=70, y=40)

            if animal.pregnant:
                label_string = "Sex: {}+1".format(animal.phenotype.trait_value_dict['Sex'])
            else:
                label_string = "Sex: {}".format(animal.phenotype.trait_value_dict['Sex'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=70)
            label_string = "Age: {}".format(animal.age)
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=85)
            label_string = "Size: {:.01f}/{}".format(animal.current_size, animal.phenotype.trait_value_dict['Max Size'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=100)
            label_string = "Orientation: {}".format(animal.orientation)
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=115)
            label_string = "Health: {:0.3f}".format(animal.drive_system.drive_value_array[0])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=140)
            label_string = "Energy: {:0.3f}".format(animal.drive_system.drive_value_array[1])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=155)
            label_string = "Arousal: {:0.3f}".format(animal.drive_system.drive_value_array[2])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=170)


            label_string = "Neural Network Properties"
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11 bold", anchor=tk.W)
            animal_text_label.place(x=30, y=200)
            label_string = "Hidden Units: {}".format(animal.nervous_system.h_size)
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=215)
            label_string = "Prediction Learning Rate: {:0.5f}".format(animal.phenotype.trait_value_dict['Prediction Learning Rate'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=230)
            label_string = "Weight Init Stdev: {:0.5f}".format(animal.phenotype.trait_value_dict['Weight Init Stdev'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=245)

            label_string = "Drive Learning Info   Target   ValueLR   ChangeLR"
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11 bold", anchor=tk.W)
            animal_text_label.place(x=30, y=275)
            label_string = "{:14s}        {:0.5f}  {:0.5f}   {:0.5f}".format("Health",
                                                                   animal.phenotype.trait_value_dict['Health Value Target'],
                                                                   animal.phenotype.trait_value_dict['Health Learning Rate'],
                                                                   animal.phenotype.trait_value_dict['HealthD Learning Rate'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=290)
            label_string = "{:14s}        {:0.5f}  {:0.5f}   {:0.5f}".format("Energy",
                                                                   animal.phenotype.trait_value_dict['Energy Value Target'],
                                                                   animal.phenotype.trait_value_dict['Energy Learning Rate'],
                                                                   animal.phenotype.trait_value_dict['EnergyD Learning Rate'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=305)
            label_string = "{:14s}        {:0.5f}  {:0.5f}   {:0.5f}".format("Arousal",
                                                                   animal.phenotype.trait_value_dict['Arousal Value Target'],
                                                                   animal.phenotype.trait_value_dict['Arousal Learning Rate'],
                                                                   animal.phenotype.trait_value_dict['ArousalD Learning Rate'])
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            animal_text_label.place(x=30, y=320)


            neural_input_state, neural_hidden_state, neural_output_state = animal.nervous_system.neural_feedforward()
            action_outputs = neural_output_state[animal.nervous_system.a_indexes[0]:animal.nervous_system.a_indexes[1] + 1]
            animal.action_system.get_legal_action_probabilities(action_outputs)
            label_string = "Action Info   Act      Prob"
            animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11 bold", anchor=tk.W)
            animal_text_label.place(x=180, y=70)
            for j in range(animal.action_system.num_actions):
                label_string = "{:12s} {:6.3f}   {:6.3f}".format(animal.action_system.action_list[j]+':',
                                                                 action_outputs[j],
                                                                 animal.action_system.legal_action_prob_distribution[j])
                animal_text_label = tk.Label(animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
                animal_text_label.place(x=180, y=90+j*16)

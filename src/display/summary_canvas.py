import tkinter as tk
from src.display import species_info_window

class SummaryCanvas(tk.Canvas):
    ############################################################################################################
    def __init__(self, display):
        tk.Canvas.__init__(self,
                           width=display.summary_canvas_width,
                           height=display.summary_canvas_height,
                           bg="grey", bd=0, highlightthickness=0)

        self.display = display
        self.summary_canvas_width = display.summary_canvas_width
        self.summary_canvas_height = display.summary_canvas_height

    ############################################################################################################
    def update_summary_display(self):
        # create the summary display frame
        self.summary_frame = tk.Frame(self,
                                      width=self.summary_canvas_width - 20,
                                      height=self.summary_canvas_height - 20,
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
        if 'Grass' in self.display.the_world.turn_summary_dict['Plant']:
            grass_data = self.display.the_world.turn_summary_dict['Plant']['Grass']
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

        if 'Zebra' in self.display.the_world.turn_summary_dict['Animal']:
            zebra_data = self.display.the_world.turn_summary_dict['Animal']['Zebra']
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

        if 'Lion' in self.display.the_world.turn_summary_dict['Animal']:
            lion_data = self.display.the_world.turn_summary_dict['Animal']['Lion']
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
    def animal_summary_on_double_click(self, event):
        print("Species click event", event)
        species = 'Zebra'
        if self.display.species_summary_window is not None:
            self.display.species_summary_window.destroy()
        self.display.species_summary_window = tk.Toplevel(self.display.root)
        self.species_summary_window_instance = species_info_window.SpeciesInfoWindow(self.display.species_summary_window,
                                                                                     self.display.the_world, species)





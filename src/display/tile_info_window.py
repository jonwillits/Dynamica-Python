import tkinter as tk
from src.display import phenotype_window


class TileInfoWindow:
    ############################################################################################################
    def __init__(self, display, tile_info_window, the_world, grid_location):
        self.display = display
        self.tile_info_window = tile_info_window
        self.tile_info_window.title("Dynamica: ({},{}) Information".format(grid_location[0], grid_location[1]))
        self.window_height = 800
        self.window_width = 400
        self.the_world = the_world

        self.terrain_frame = None
        self.terrain_header = None
        self.terrain_image_label = None
        self.terrain_image = None
        self.terrain_text_label = None

        self.plant_frame = None
        self.plant_header = None
        self.plant_image_label = None
        self.plant_image = None
        self.plant_text_label = None

        self.object_frame = None
        self.object_header = None
        self.object_image_label = None
        self.object_image = None
        self.object_text_label = None

        self.animal_frame = None
        self.animal_header = None
        self.animal_image_label = None
        self.animal_image = None
        self.animal_text_label1 = None
        self.animal_text_label2 = None
        self.animal_text_label3 = None
        self.animal_text_label4 = None
        self.animal_text_label5 = None
        self.animal_text_label6 = None
        self.animal_text_label7 = None
        self.animal_text_label8 = None

        self.phenotype_label = None
        self.phenotype_window = None
        self.phenotype_window_instance = None

        self.action_label = None
        self.action_window = None
        self.action_window_instance = None

        self.neural_network_label = None
        self.neural_network_window = None
        self.neural_network_window_instance = None

        self.info_canvas = tk.Canvas(self.tile_info_window, width=self.window_width, height=self.window_height)
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
        self.terrain_frame = tk.Frame(self.info_canvas, width=400, height=100)
        self.terrain_frame.grid(row=0, column=0)

        self.terrain_header = tk.Label(self.terrain_frame, text="Terrain Information", font="Verdana 12 bold")
        self.terrain_header.place(x=10, y=10)

        self.terrain_image = tk.PhotoImage(file=self.the_world.map[grid_location].image)
        self.terrain_image_label = tk.Label(self.terrain_frame, image=self.terrain_image, anchor=tk.W)
        self.terrain_image_label.place(x=30, y=30)

        self.terrain_text_label = tk.Label(self.terrain_frame, text=self.the_world.map[grid_location].terrain_type,
                                           font="Verdana 11", anchor=tk.W)
        self.terrain_text_label.place(x=70, y=40)

    ############################################################################################################
    def get_plant_info(self, grid_location):
        self.plant_frame = tk.Frame(self.info_canvas, width=400, height=100)
        self.plant_frame.grid(row=1, column=0)

        self.plant_header = tk.Label(self.plant_frame, text="Vegetation Information", font="Verdana 12 bold")
        self.plant_header.place(x=10, y=10)

        if len(self.the_world.map[grid_location].plant_list) == 0:
            plant_string = "None"
        else:
            plant = self.the_world.map[grid_location].plant_list[0]
            plant_string = "{}: {}".format(plant.species, plant.quantity)

        self.plant_text_label = tk.Label(self.plant_frame, text=plant_string, font="Verdana 11")
        self.plant_text_label.place(x=30, y=40)

    ############################################################################################################
    def get_object_info(self, grid_location):
        self.object_frame = tk.Frame(self.info_canvas, width=400, height=100)
        self.object_frame.grid(row=2, column=0)

        self.object_header = tk.Label(self.object_frame, text="Object Information", font="Verdana 12 bold")
        self.object_header.place(x=10, y=10)
        if len(self.the_world.map[grid_location].object_list) == 0:
            object_string = "None"
        else:
            world_object = self.the_world.map[grid_location].object_list[0]
            object_string = "{}: {}".format(world_object.object_type, world_object.quantity)

        self.object_text_label = tk.Label(self.object_frame, text=object_string, font="Verdana 11")
        self.object_text_label.place(x=30, y=40)

    ############################################################################################################
    def get_animal_info(self, grid_location):
        self.animal_frame = tk.Frame(self.info_canvas, width=400, height=500)
        self.animal_frame.grid(row=3, column=0)

        self.animal_header = tk.Label(self.animal_frame, text="Animal Information", font="Verdana 12 bold")
        self.animal_header.place(x=10, y=10)

        if len(self.the_world.map[grid_location].animal_list) == 0:
            self.animal_text_label1 = tk.Label(self.animal_frame, text="None", font="Verdana 11 bold")
            self.animal_text_label1.place(x=30, y=30)
        else:
            animal = self.the_world.map[grid_location].animal_list[0]
            label_string = "{} {}".format(animal.species, animal.id_number)
            self.animal_image = tk.PhotoImage(file=animal.image_dict[0])
            self.animal_image_label = tk.Label(self.animal_frame, image=self.animal_image, anchor=tk.W)
            self.animal_image_label.place(x=30, y=30)
            self.animal_text_label1 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label1.place(x=70, y=40)

            if animal.pregnant:
                label_string = "Sex: {}+1".format(animal.phenotype.trait_value_dict['Sex'])
            else:
                label_string = "Sex: {}".format(animal.phenotype.trait_value_dict['Sex'])
            self.animal_text_label2 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label2.place(x=30, y=70)
            label_string = "Age: {}".format(animal.age)
            self.animal_text_label3 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label3.place(x=30, y=85)
            label_string = "Size: {:.01f}/{}".format(animal.current_size, animal.phenotype.trait_value_dict['Max Size'])
            self.animal_text_label4 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label4.place(x=30, y=100)
            label_string = "Orientation: {}".format(animal.orientation)
            self.animal_text_label5 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label5.place(x=30, y=115)

            label_string = "Health: {:0.3f}".format(animal.drive_system.drive_value_array[0])
            self.animal_text_label6 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label6.place(x=180, y=70)
            label_string = "Energy: {:0.3f}".format(animal.drive_system.drive_value_array[1])
            self.animal_text_label7 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label7.place(x=180, y=85)
            label_string = "Arousal: {:0.3f}".format(animal.drive_system.drive_value_array[2])
            self.animal_text_label8 = tk.Label(self.animal_frame, text=label_string, font="Courier 11", anchor=tk.W)
            self.animal_text_label8.place(x=180, y=100)

            self.phenotype_label = tk.Label(self.animal_frame, text='View Phenotype', font="Courier 11 bold",
                                            anchor=tk.W)
            self.phenotype_label.place(x=30, y=145)
            self.phenotype_label.bind('<Double-Button-1>',
                                      lambda event, arg=animal: self.view_phenotype_on_double_click(event, arg))

            self.action_label = tk.Label(self.animal_frame, text='View Action System', font="Courier 11 bold",
                                         anchor=tk.W)
            self.action_label.place(x=30, y=165)
            self.action_label.bind('<Double-Button-1>',
                                   lambda event, arg=animal: self.view_actions_on_double_click(event, arg))

            self.neural_network_label = tk.Label(self.animal_frame, text='View Neural Network', font="Courier 11 bold",
                                                 anchor=tk.W)
            self.neural_network_label.place(x=30, y=185)
            self.neural_network_label.bind('<Double-Button-1>',
                                           lambda event, arg=animal: self.view_neural_network_on_double_click(event,
                                                                                                              arg))

    ############################################################################################################
    def view_phenotype_on_double_click(self, event, animal):
        self.phenotype_window = tk.Toplevel(self.display.root)
        self.phenotype_window_instance = phenotype_window.PhenotypeWindow(self.phenotype_window, animal)

    ############################################################################################################
    def view_actions_on_double_click(self, event, animal):
        pass

    ############################################################################################################
    def view_neural_network_on_double_click(self, event, animal):
        pass

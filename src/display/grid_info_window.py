import tkinter as tk


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

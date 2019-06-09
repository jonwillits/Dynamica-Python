import tkinter as tk
import math


class NeuralNetworkWindow:
    ############################################################################################################
    def __init__(self, neural_network_window, animal):

        self.root = neural_network_window
        self.root.resizable(0, 0)
        self.a = animal
        self.root.title("{} {} Neural Network".format(self.a.species, self.a.id_number))

        self.width = 1600
        self.height = 1200

        # create the canvas and scrollbar
        self.input_frame = tk.Frame(self.root, height=1200, width=550)
        self.hidden_frame = tk.Frame(self.root, height=1200, width=500)
        self.output_frame = tk.Frame(self.root, height=1200, width=550)
        self.input_frame.grid(row=0, column=0)
        self.hidden_frame.grid(row=0, column=1)
        self.output_frame.grid(row=0, column=2)

        # get the neural network data
        self.input_state, self.h, self.output_state = self.a.nervous_system.neural_feedforward()

        self.s_in = self.input_state[self.a.nervous_system.s_indexes[0]:self.a.nervous_system.s_indexes[1] + 1]
        self.d_in = self.input_state[self.a.nervous_system.d_indexes[0]:self.a.nervous_system.d_indexes[1] + 1]
        self.a_in = self.input_state[self.a.nervous_system.a_indexes[0]:self.a.nervous_system.a_indexes[1] + 1]
        self.aa_in = self.input_state[self.a.nervous_system.aa_indexes[0]:self.a.nervous_system.aa_indexes[1] + 1]
        start = self.a.nervous_system.last_h_indexes[0]
        stop = self.a.nervous_system.last_h_indexes[1] + 1
        self.last_h_in = self.input_state[start:stop]

        self.s_out = self.output_state[self.a.nervous_system.s_indexes[0]:self.a.nervous_system.s_indexes[1] + 1]
        self.d_out = self.output_state[self.a.nervous_system.d_indexes[0]:self.a.nervous_system.d_indexes[1] + 1]
        self.a_out = self.output_state[self.a.nervous_system.a_indexes[0]:self.a.nervous_system.a_indexes[1] + 1]
        self.aa_out = self.output_state[self.a.nervous_system.aa_indexes[0]:self.a.nervous_system.aa_indexes[1] + 1]

        self.input_rect_list = []

        self.show_input_layer()
        self.show_output_layer()
        self.show_hidden_layer()

    ############################################################################################################
    @staticmethod
    def get_hex_color(value):
        abs_value = 1 - abs(value)
        scaled_value = int(round(255*abs_value, 0))
        hex_value = hex(scaled_value)[2:]

        if len(hex_value) == 1:
            hex_value = "0" + hex_value

        if value > 0:
            return '#{}ff{}'.format(hex_value, hex_value)
        elif value < 0:
            return '#ff{}{}'.format(hex_value, hex_value)
        else:
            return "#ffffff"

    ############################################################################################################
    def show_input_layer(self):

        label_x = 10
        label_spacing = 15
        box_x = 70
        box_size = 10
        box_spacing = 15

        self.input_title = tk.Label(self.input_frame, text="Input Layer", font="Courier 18 bold", bd=0, padx=0, pady=0)
        self.input_title.place(x=10, y=10)

        start_y = 30
        self.drive_title = tk.Label(self.input_frame, text="Drive States", font="Courier 14 bold", bd=0, padx=0, pady=0)
        self.drive_title.place(x=10, y=start_y)
        for i in range(self.a.drive_system.num_drives):
            drive = self.a.drive_system.drive_list[i]
            drive_input_value = self.d_in[i]
            hex_color = self.get_hex_color(drive_input_value)

            self.drive_label = tk.Label(self.input_frame, text=drive, font="Courier 10", bd=0, padx=0, pady=0)
            self.drive_label.place(x=label_x, y=start_y+15+i*label_spacing)

            self.box_frame = tk.Frame(self.input_frame, height=box_size, width=box_size)
            self.box_frame.pack_propagate(0)
            self.box_frame.place(x=box_x, y=start_y+15+i*box_spacing)

            self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                      bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
            self.drive_box.pack(fill=tk.BOTH, expand=1)

        start_y = 95
        self.action_title = tk.Label(self.input_frame, text="Last Action", font="Courier 14 bold", bd=0, padx=0, pady=0)
        self.action_title.place(x=10, y=start_y)
        for i in range(self.a.action_system.num_actions):
            action = self.a.action_system.action_list[i]
            action_input_value = self.a_in[i]
            hex_color = self.get_hex_color(action_input_value)

            self.action_label = tk.Label(self.input_frame, text=action, font="Courier 10", bd=0, padx=0, pady=0)
            self.action_label.place(x=label_x, y=start_y+15+i*label_spacing)

            self.box_frame = tk.Frame(self.input_frame, height=box_size, width=box_size)
            self.box_frame.pack_propagate(0)
            self.box_frame.place(x=box_x, y=start_y+15+i*box_spacing)

            self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                      bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
            self.drive_box.pack(fill=tk.BOTH, expand=1)

        start_y = 205
        box_x = 10
        box_spacing = 10
        self.action_arg_title = tk.Label(self.input_frame, text="Last Action Argument", font="Courier 14 bold",
                                         bd=0, padx=0, pady=0)
        self.action_arg_title.place(x=10, y=start_y)
        for i in range(3):
            for j in range(10):
                action_input_value = self.aa_in[j+10*i]
                hex_color = self.get_hex_color(action_input_value)

                self.box_frame = tk.Frame(self.input_frame, height=box_size, width=box_size)
                self.box_frame.pack_propagate(0)
                self.box_frame.place(x=box_x+j*box_spacing, y=start_y + 15 + i * box_spacing)

                self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                          bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
                self.drive_box.pack(fill=tk.BOTH, expand=1)

        start_y = 260
        view_list = self.a.nervous_system.get_view_list()
        self.sensory_title = tk.Label(self.input_frame, text="Sensory State", font="Courier 14 bold", bd=0,
                                      padx=0, pady=0)
        self.sensory_title.place(x=10, y=start_y)

        for i in range(5):
            view_list_text = 'Tile {}'.format(view_list[i])
            view_list_label = tk.Label(self.input_frame, text=view_list_text, font="Courier 12 bold", bd=0, padx=0, pady=0)
            view_list_label.place(x=10, y=start_y+i*70+20)

            view_type_text = "Terrain"
            view_list_label = tk.Label(self.input_frame, text="Terrain", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=10, y=start_y+i*70+35)
            view_list_label = tk.Label(self.input_frame, text="Animal", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=130, y=start_y+i*70+35)
            view_list_label = tk.Label(self.input_frame, text="Plant", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=250, y=start_y+i*70+35)
            view_list_label = tk.Label(self.input_frame, text="Object", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=370, y=start_y+i*70+35)

            for j in range(4):
                for m in range(3):
                    for n in range(10):
                        index = 120*i + 30*j + 10*m + n
                        action_input_value = self.s_in[index]
                        hex_color = self.get_hex_color(action_input_value)

                        xcoord = box_x + n*box_spacing + 120*j
                        ycoord = start_y + 15 + m*box_spacing + i*70 + 30

                        self.box_frame = tk.Frame(self.input_frame, height=box_size, width=box_size)
                        self.box_frame.pack_propagate(0)
                        self.box_frame.place(x=xcoord, y=ycoord)

                        self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                                  bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
                        self.drive_box.pack(fill=tk.BOTH, expand=1)

    ############################################################################################################
    def show_hidden_layer(self):
        box_x = 20
        box_y = 30
        box_size = 10
        box_spacing = 10

        self.hidden_title = tk.Label(self.hidden_frame, text="Hidden Layer",
                                     font="Courier 18 bold", bd=0, padx=0, pady=0)
        self.hidden_title.place(x=10, y=10)

        self.recurrent_title = tk.Label(self.hidden_frame, text="Recurrent Layer",
                                     font="Courier 18 bold", bd=0, padx=0, pady=0)
        self.recurrent_title.place(x=10, y=610)
        h_size = self.a.nervous_system.h_size

        num_cols = math.ceil(h_size / 50.0)
        for i in range(num_cols):
            for j in range(50):
                index = i * 50 + j
                if index < h_size:
                    xcoord = box_x + box_spacing * i
                    ycoord1 = box_y + box_spacing * j
                    ycoord2 = box_y + box_spacing * j + 600
                    hidden_value = self.h[index]
                    hex_color1 = self.get_hex_color(hidden_value)
                    recurrent_value = self.last_h_in[index]
                    hex_color2 = self.get_hex_color(recurrent_value)

                    self.box_frame = tk.Frame(self.hidden_frame, height=box_size, width=box_size)
                    self.box_frame.pack_propagate(0)
                    self.box_frame.place(x=xcoord, y=ycoord1)

                    self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                              bd=1, padx=0, pady=0, bg=hex_color1, relief='solid')
                    self.drive_box.pack(fill=tk.BOTH, expand=1)

                    self.box_frame = tk.Frame(self.hidden_frame, height=box_size, width=box_size)
                    self.box_frame.pack_propagate(0)
                    self.box_frame.place(x=xcoord, y=ycoord2)

                    self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                              bd=1, padx=0, pady=0, bg=hex_color2, relief='solid')
                    self.drive_box.pack(fill=tk.BOTH, expand=1)

    ############################################################################################################
    def show_output_layer(self):

        label_x = 10
        label_spacing = 15
        box_x = 70
        box_size = 10
        box_spacing = 15

        output_title = tk.Label(self.output_frame, text="Output Layer", font="Courier 18 bold", bd=0, padx=0, pady=0)
        output_title.place(x=10, y=10)

        start_y = 30
        drive_title = tk.Label(self.output_frame, text="Drive States", font="Courier 14 bold", bd=0, padx=0, pady=0)
        drive_title.place(x=10, y=start_y)
        for i in range(self.a.drive_system.num_drives):
            drive = self.a.drive_system.drive_list[i]
            drive_input_value = self.d_out[i]
            hex_color = self.get_hex_color(drive_input_value)

            self.drive_label = tk.Label(self.output_frame, text=drive, font="Courier 10", bd=0, padx=0, pady=0)
            self.drive_label.place(x=label_x, y=start_y+15+i*label_spacing)

            self.box_frame = tk.Frame(self.output_frame, height=box_size, width=box_size)
            self.box_frame.pack_propagate(0)
            self.box_frame.place(x=box_x, y=start_y+15+i*box_spacing)

            self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                      bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
            self.drive_box.pack(fill=tk.BOTH, expand=1)

        start_y = 95
        self.action_title = tk.Label(self.output_frame, text="Last Action", font="Courier 14 bold", bd=0, padx=0, pady=0)
        self.action_title.place(x=10, y=start_y)
        for i in range(self.a.action_system.num_actions):
            action = self.a.action_system.action_list[i]
            action_input_value = self.a_out[i]
            hex_color = self.get_hex_color(action_input_value)

            self.action_label = tk.Label(self.output_frame, text=action, font="Courier 10", bd=0, padx=0, pady=0)
            self.action_label.place(x=label_x, y=start_y+15+i*label_spacing)

            self.box_frame = tk.Frame(self.output_frame, height=box_size, width=box_size)
            self.box_frame.pack_propagate(0)
            self.box_frame.place(x=box_x, y=start_y+15+i*box_spacing)

            self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                      bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
            self.drive_box.pack(fill=tk.BOTH, expand=1)

        start_y = 205
        box_x = 10
        box_spacing = 10
        self.action_arg_title = tk.Label(self.output_frame, text="Last Action Argument", font="Courier 14 bold",
                                         bd=0, padx=0, pady=0)
        self.action_arg_title.place(x=10, y=start_y)
        for i in range(3):
            for j in range(10):
                action_input_value = self.aa_out[j+10*i]
                hex_color = self.get_hex_color(action_input_value)

                self.box_frame = tk.Frame(self.output_frame, height=box_size, width=box_size)
                self.box_frame.pack_propagate(0)
                self.box_frame.place(x=box_x+j*box_spacing, y=start_y + 15 + i * box_spacing)

                self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                          bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
                self.drive_box.pack(fill=tk.BOTH, expand=1)

        start_y = 260
        view_list = self.a.nervous_system.get_view_list()
        self.sensory_title = tk.Label(self.output_frame, text="Sensory State", font="Courier 14 bold", bd=0,
                                      padx=0, pady=0)
        self.sensory_title.place(x=10, y=start_y)

        for i in range(5):
            view_list_text = 'Tile {}'.format(view_list[i])
            view_list_label = tk.Label(self.output_frame, text=view_list_text, font="Courier 12 bold", bd=0, padx=0, pady=0)
            view_list_label.place(x=10, y=start_y+i*70+20)

            view_type_text = "Terrain"
            view_list_label = tk.Label(self.output_frame, text="Terrain", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=10, y=start_y+i*70+35)
            view_list_label = tk.Label(self.output_frame, text="Animal", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=130, y=start_y+i*70+35)
            view_list_label = tk.Label(self.output_frame, text="Plant", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=250, y=start_y+i*70+35)
            view_list_label = tk.Label(self.output_frame, text="Object", font="Courier 10", bd=0, padx=0, pady=0)
            view_list_label.place(x=370, y=start_y+i*70+35)

            for j in range(4):
                for m in range(3):
                    for n in range(10):
                        index = 120*i + 30*j + 10*m + n
                        action_input_value = self.s_out[index]
                        hex_color = self.get_hex_color(action_input_value)

                        xcoord = box_x + n*box_spacing + 120*j
                        ycoord = start_y + 15 + m*box_spacing + i*70 + 30

                        self.box_frame = tk.Frame(self.output_frame, height=box_size, width=box_size)
                        self.box_frame.pack_propagate(0)
                        self.box_frame.place(x=xcoord, y=ycoord)

                        self.drive_box = tk.Label(self.box_frame, height=box_size, width=box_size,
                                                  bd=1, padx=0, pady=0, bg=hex_color, relief='solid')
                        self.drive_box.pack(fill=tk.BOTH, expand=1)













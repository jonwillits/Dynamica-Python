import tkinter as tk
import os
import sys
from src import config
from src.display import button_canvas, summary_canvas, main_frame
import time


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

        self.main_frame = None
        self.main_canvas = None
        self.main_canvas_height = self.root_height - 50
        self.main_canvas_width = self.root_width - 500 - 15

        self.summary_canvas = None
        self.summary_canvas_height = self.root_height - 35
        self.summary_canvas_width = 500

        self.species_summary_window = None

        self.tile_info_window = None
        self.tile_info_window_instance = None

        self.button_canvas = None
        self.button_canvas_height = 20
        self.button_canvas_width = self.root_width

        self.configure_sizes()
        self.create_main_window()
        self.create_main_frame()
        self.create_summary_canvas()

        self.create_buttons()

        self.load_images()
        self.main_frame.draw_terrain()
        self.main_frame.draw_objects()
        self.main_frame.draw_animals()
        self.summary_canvas.update_summary_display()

        self.start_time = time.time()

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
    def create_main_frame(self):
        self.main_frame = main_frame.MainFrame(self)
        self.main_frame.grid(row=0, column=0)

    ############################################################################################################
    def create_summary_canvas(self):
        self.summary_canvas = summary_canvas.SummaryCanvas(self)
        self.summary_canvas.grid(row=0, column=1, padx=0, pady=0, ipadx=0, ipady=0)

    ############################################################################################################
    def create_buttons(self):
        self.button_canvas = button_canvas.ButtonCanvas(self)
        self.button_canvas.grid(row=1, column=0, columnspan=2, padx=0, pady=0, ipadx=0, ipady=0)

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
    def run_game(self):
        if self.running:
            self.running = False
            self.button_canvas.run_button.config(text="Run")
        else:
            self.running = True
            self.button_canvas.run_button.config(text="Pause")

        while self.running:
            self.next_turn()

    ############################################################################################################
    def next_turn(self):

        self.turn += 1
        self.root.title("Dynamica: Turn {}".format(self.turn))
        self.the_world.next_turn()
        self.main_frame.main_canvas.delete("all")
        self.main_frame.draw_terrain()
        self.main_frame.draw_objects()
        self.main_frame.draw_animals()
        self.summary_canvas.update_summary_display()
        self.root.update()
        self.root.update_idletasks()
        if self.turn % 10 == 0:
            took = time.time() - self.start_time
            self.start_time = time.time()
            print(took)



    ############################################################################################################
    def save_game(self):
        pass

    ############################################################################################################
    def quit_game(self):
        if self.running:
            self.run_game()
        sys.exit(1)

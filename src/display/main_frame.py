import tkinter as tk
from src.display import grid_info_window


class MainFrame(tk.Frame):
    ############################################################################################################
    def __init__(self, display):
        super().__init__()

        self.display = display
        self.tile_info_window = None
        self.tile_info_window_instance = None
        self.terrain_image_dict = {}

        self.main_canvas = tk.Canvas(self,
                                     height=display.main_canvas_height, width=display.main_canvas_width,
                                     bd=0, highlightthickness=0, bg='#000000',
                                     scrollregion=(0, 0, display.main_canvas_width, display.main_canvas_height))

        self.game_frame = tk.Frame(self.main_canvas)
        self.game_frame.grid(row=0, column=0)

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.main_canvas.yview)
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.main_canvas.xview)
        self.main_canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.grid(sticky=tk.N+tk.S+tk.E)
        self.hsb.grid(sticky=tk.E+tk.W+tk.S)
        self.main_canvas.grid(row=0, column=0)
        self.main_canvas.create_window((4, 4), window=self.game_frame, anchor="nw")

        self.game_frame.bind("<Configure>", lambda event, canvas=self.main_canvas: self.on_frame_configure(canvas))

        self.main_canvas.bind('<Double-Button-1>', self.main_canvas_on_double_click)

    ############################################################################################################
    @staticmethod
    def on_frame_configure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    ############################################################################################################
    def main_canvas_on_double_click(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        self.show_tile_click_info(x, y)

    ############################################################################################################
    def show_tile_click_info(self, x, y):
        grid_x, grid_y = self.get_grid_coordinates(x, y)
        if 0 <= grid_x <= self.display.num_columns - 1:
            if 0 <= grid_y <= self.display.num_rows - 1:
                if self.tile_info_window is not None:
                    self.tile_info_window.destroy()
                self.tile_info_window = tk.Toplevel(self.display.root)
                self.tile_info_window_instance = grid_info_window.GridInfoWindow(self.tile_info_window,
                                                                                 self.display.the_world,
                                                                                 (grid_x, grid_y))

    ############################################################################################################
    def get_screen_coordinates(self, grid_x, grid_y):
        screen_x = grid_x * self.display.grid_size
        screen_y = grid_y * self.display.grid_size
        return screen_x, screen_y

    ############################################################################################################
    def get_grid_coordinates(self, screen_x, screen_y):
        grid_x = int(round((screen_x - self.display.grid_size/2) / self.display.grid_size))
        grid_y = int(round((screen_y - self.display.grid_size/2) / self.display.grid_size))
        return grid_x, grid_y

    ############################################################################################################
    def draw_terrain(self):
        for i in range(self.display.the_world.num_rows):
            for j in range(self.display.the_world.num_columns):
                current_tile = self.display.the_world.map[(j, i)]
                x, y = self.get_screen_coordinates(j, i)

                self.main_canvas.create_image(x, y, anchor=tk.NW, image=self.display.image_dict[current_tile.image])

    ############################################################################################################
    def draw_animals(self):
        for animal in self.display.the_world.animal_list:
            x, y = self.get_screen_coordinates(animal.position[0], animal.position[1])
            image = animal.image_dict[animal.orientation]
            self.main_canvas.create_image(x+2, y+2, anchor=tk.NW, image=self.display.image_dict[image])

    ############################################################################################################
    def draw_objects(self):
        for world_object in self.display.the_world.object_list:
            x, y = self.get_screen_coordinates(world_object.position[0], world_object.position[1])
            image = world_object.graphic_object
            self.main_canvas.create_image(x+6, y+6, anchor=tk.NW, image=self.display.image_dict[image])

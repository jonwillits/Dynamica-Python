import tkinter as tk


class PlotSpeciesInfo:
    ############################################################################################################
    def __init__(self, master, data, display):
        self.window_width = 600
        self.window_height = 600

        self.master = master
        self.master.title(data[0])

        self.canvas = tk.Canvas(self.master, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        self.canvas.create_line(30, 30, 30, 570, width=2)
        self.canvas.create_line(30, 570, 570, 570, width=2)
        self.display = display

        for i in range(19):
            x = 30 + (i * 30)
            self.canvas.create_line(x, 570, x, 570, width=2)
        self.canvas.create_text(300, 585, text='Turn')

        for i in range(19):
            y = 570 - (i * 30)
            self.canvas.create_line(30, y, 30, y, width=2)
        self.canvas.create_text(15, 275, text=data[1])

        self.x_list = []
        self.y_list = data[2]
        self.x_list.append(1)
        for i in range(2, len(self.y_list)):
            self.x_list.append(i)

        self.convert_scales()

    ############################################################################################################
    def convert_scales(self):
        if len(self.x_list) and len(self.y_list) == 1:
            self.canvas.create_line(self.x_list[0], self.y_list[0], self.x_list[0] + 5, self.y_list[0], width=2)
            self.canvas.create_line(self.x_list[0] + 5, self.y_list[0], self.x_list[0] + 10, self.y_list[0], width=2)
            self.display.root.update()
        else:
            pixel_x = []
            pixel_y = []

            x_max = self.x_list[0]
            y_max = self.y_list[0]
            x_min = self.x_list[0]
            y_min = self.y_list[0]

            for i in range(len(self.x_list)):
                if self.x_list[i] >= x_max:
                    x_max = self.x_list[i]

            for i in range(len(self.y_list)):
                if self.y_list[i] >= y_max:
                    y_max = self.y_list[i]

            for i in range(len(self.x_list)):
                if self.x_list[i] <= x_min:
                    x_min = self.x_list[i]

            for i in range(len(self.y_list)):
                if self.y_list[i] <= y_min:
                    y_min = self.y_list[i]

            self.canvas.create_text(15, 30, text = y_max)
            # self.canvas.create_text(100, 15, text=y_max)
            self.canvas.create_text(15, 165, text = '75%')
            self.canvas.create_text(15, 300, text = '50%')
            self.canvas.create_text(15, 435, text = '25%')
            self.canvas.create_text(15, 570, text = '0%')

            self.canvas.create_text(30, 585, text = '0%')
            self.canvas.create_text(138, 585, text = '20%')
            self.canvas.create_text(246, 585, text = '40%')
            self.canvas.create_text(354, 585, text = '60%')
            self.canvas.create_text(462, 585, text = '80%')
            self.canvas.create_text(570, 585, text = x_max)

            x_range = x_max - x_min
            y_range = y_max - y_min

            if y_range == 0 and y_max <= 1:
                for i in range(1, len(self.y_list)):
                    pixel_y.append(self.y_list[i] * 540)
            else:
                if y_range == 0 and y_max > 1:
                    for i in range(len(self.y_list)):
                        pixel_y.append(570)
                else:
                    y_distance = 540 / y_range
                    pixel_y.append((self.y_list[0] - y_min) * y_distance)

                    for i in range(1, len(self.y_list)):
                        pixel_y.append(pixel_y[i - 1] + (self.y_list[i] - self.y_list[i - 1]) * y_distance)

            x_distance = 540 / x_range
            pixel_x.append((self.x_list[0] - x_min) * x_distance)

            for i in range(1, len(self.x_list)):
                pixel_x.append(pixel_x[i - 1] + (self.x_list[i] - self.x_list[i - 1]) * x_distance)

            print(pixel_x, pixel_y)
            self.plot_graph(pixel_x, pixel_y)

    ############################################################################################################
    def plot_graph(self, pixel_x, pixel_y):
        for i in range(len(pixel_y)):
            self.canvas.create_line(30 + pixel_x[i], 570 - pixel_y[i], 30 + pixel_x[i + 1], 570 - pixel_y[i + 1],
                                    width=2)
            self.canvas.create_line(30 + pixel_x[i + 1], 570 - pixel_y[i + 1], 30 + pixel_x[i + 2], 570 - pixel_y[i + 2]
                                    , width=2)
            self.display.root.update()
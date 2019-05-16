import tkinter as tk
import random
import sys
import time


class Application:

	def __init__(self):

		self.num_rows = 20
		self.num_columns = 24
		self.num_animals = 50

		self.root = tk.Tk()
		self.main_canvas = tk.Canvas(self.root, width=800, height=600)
		self.main_canvas.grid(row=0, column=0)
		self.terrain_image = tk.PhotoImage(file='plains.gif')
		self.animal_image = tk.PhotoImage(file='zebra.gif')

		self.button_canvas = tk.Canvas(self.root, width=800, height=100)
		self.button_canvas.grid(row=1, column=0)
		self.run_button = tk.Button(self.button_canvas, text="Run", fg="black", height=2, width=8, command=self.run)
		self.run_button.grid(row=0, column=0, sticky=tk.E)

		self.quit_button = tk.Button(self.button_canvas, text="Quit", fg="black", height=2, width=8, command=sys.exit)
		self.quit_button.grid(row=0, column=1, sticky=tk.E)

		self.running = False
		self.turn = 0
		self.took = 0
		
		self.next_turn()

	def run(self):
		if self.running:
			self.running = False
			self.run_button.config(text="Run")
		else:
			self.running = True
			self.run_button.config(text="Pause")

		while self.running:
			self.next_turn()

	def next_turn(self):
		self.turn += 1
		self.root.title("Turn {} Took {:0.3f}".format(self.turn, self.took))
		start_time = time.time()
		self.main_canvas.delete("all")

		for i in range(self.num_rows):
			for j in range(self.num_columns):
				self.main_canvas.create_image(j*32, i*32, anchor=tk.NW, image=self.terrain_image)

		for i in range(self.num_animals):
			x = random.randint(0,self.num_rows-1)
			y = random.randint(0,self.num_columns-1)
			self.main_canvas.create_image(y*32+4, x*32+4, anchor=tk.NW, image=self.animal_image)

		self.root.update()
		self.took = time.time() - start_time


def main():
	app = Application()
	app.root.mainloop()


main()

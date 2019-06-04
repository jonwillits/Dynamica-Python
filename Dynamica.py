from src.display import display
from src import world
import sys


def main():
	if len(sys.argv) > 1:
		save_file = sys.argv[1]
	else:
		save_file = None

	the_world = world.World(save_file)
	gw = display.Display(the_world)
	gw.root.mainloop()


main()

from src.display import display
from src import world


def main():
    the_world = world.World()
    gw = display.Display(the_world)
    gw.root.mainloop()


main()

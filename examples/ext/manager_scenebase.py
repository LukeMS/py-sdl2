"""Shows a blank (green) scene."""

from sdl2.ext import manager


# the window's background color (RGBA, from 0-255)
WINDOW_COLOR = (0, 255, 0, 255)


if __name__ == '__main__':
    m = manager.Manager(window_color=WINDOW_COLOR)
    m.set_scene(manager.SceneBase)
    m.run()

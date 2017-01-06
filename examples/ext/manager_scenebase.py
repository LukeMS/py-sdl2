"""Utility to create a Manager instance constant values as default."""

import os


from sdl2.ext import manager


# size of a (square) tile's side in pixels.
TILE_SIZE = 32

# the width of the screen in pixels.
SCREEN_WIDTH = 1024

# the height of the screen in pixels
SCREEN_HEIGHT = 768

# maximum frames per second that should be drawn
LIMIT_FPS = 30

# the window's background color (RGBA, from 0-255)
WINDOW_COLOR = (0, 255, 0, 255)


if __name__ == '__main__':
    resources = os.path.join(os.path.dirname(__file__), "resources")
    m = manager.Manager(
        SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, LIMIT_FPS, WINDOW_COLOR,
        resources)
    m.set_scene(manager.SceneBase)
    m.run()

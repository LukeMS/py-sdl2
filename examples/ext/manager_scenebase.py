"""Shows a blank (green) scene."""

import os


from sdl2.ext import manager


# the window's background color (RGBA, from 0-255)
WINDOW_COLOR = (0, 255, 0, 255)


if __name__ == '__main__':
    resources = os.path.join(os.path.dirname(__file__), "resources")
    m = manager.Manager(window_color=WINDOW_COLOR, resources_path=resources)
    m.set_scene(manager.SceneBase)
    m.run()

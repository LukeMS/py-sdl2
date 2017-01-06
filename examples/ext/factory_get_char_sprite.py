"""..."""

import os

from sdl2.ext import manager


# the width of the screen in pixels.
SCREEN_WIDTH = 288

# the height of the screen in pixels
SCREEN_HEIGHT = 288


class RogueLike(manager.SceneBase):
    """An aspiring Roguelike game's scene."""

    def __init__(self, **kwargs):
        """Initialization."""
        self.at = self.factory.get_char_sprite("@")
        # self.at = self.factory.from_texture(self.factory._tileset)
        self.at.position = (128, 128)

    def on_update(self):
        """Graphical logic."""
        # use the render method from manager's spriterenderer
        self.manager.spriterenderer.render(sprites=self.at)


if __name__ == '__main__':
    resources = os.path.join(os.path.dirname(__file__), "resources")
    m = manager.Manager(width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                        resources_path=resources)

    # pass our created RogueLike scene to the Manager
    m.set_scene(scene=RogueLike)

    # make it fly!
    m.run()

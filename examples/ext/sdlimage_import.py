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
        # pass the name of the resource to the sdl2_ext2.Resources instance on
        # manager.py
        fname = self.resources.get_path("HalfOgreFighter3.png")

        # use the pysdl2 factory to create a sprite from an image
        self.sprite = self.factory.from_image(fname)

        print(self.sprite.position)
        print(self.sprite.x, self.sprite.y)
        # set it to a position to look better on our screenshot :)
        self.sprite.position = (128, 128)
        print(self.sprite.x, self.sprite.y)

    def on_update(self):
        """Graphical logic."""
        # use the render method from manager's spriterenderer
        self.manager.spriterenderer.render(sprites=self.sprite)


if __name__ == '__main__':
    resources = os.path.join(os.path.dirname(__file__), "resources")
    m = manager.Manager(width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                        resources_path=resources)

    # pass our created RogueLike scene to the Manager
    m.set_scene(scene=RogueLike)

    # make it fly!
    m.run()

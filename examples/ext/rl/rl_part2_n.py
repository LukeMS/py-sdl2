"""A roguelike implementation."""

import sdl2
from sdl2.ext import manager


class SceneRogueLike(manager.SceneBase):
    """A roguelike game scene."""

    def __init__(self, **kwargs):
        """Initialization."""
        # create a character using the factory
        self.player = GameObject(self, 8, 8, '@', (255, 255, 255, 255))
        npc = GameObject(self, 4, 4, '@', (255, 255, 0, 255))
        self.objects = [self.player, npc]

    def on_update(self):
        """Graphical logic."""
        # render it
        [obj.render() for obj in self.objects]

    def on_key_release(self, event, sym, mod):
        """Called on keyboard input, when a key is **released**."""
        if sym == sdl2.SDLK_ESCAPE:
            self.quit()
        elif sym == sdl2.SDLK_DOWN:
            self.player.move(0, 1)
        elif sym == sdl2.SDLK_UP:
            self.player.move(0, -1)
        elif sym == sdl2.SDLK_RIGHT:
            self.player.move(1, 0)
        elif sym == sdl2.SDLK_LEFT:
            self.player.move(-1, 0)


class GameObject(object):
    """Generic game object.

    It can represent the player, a monster, an item, the stairs, etc.
    """

    def __init__(self, scene, x, y, char, color=None, alpha=None):
        """Initialization.

        Args:
            scene (manager.SceneBase): the game scene.
            x (int): horizontal grid-relative position
            y (int): vertical grid-relative position
            char (str): string of one character to be rendered
            color (tuple): 3 rgb color int values between 0 and 255
            alpha (int): integer between 0 and 255

        Attributes:
           sprite (sdl2.ext.sprite.Sprite): the drawn sprite
        """
        self.scene = scene
        self.sprite = scene.factory.get_char_sprite(
            char, alpha_mod=alpha, color_mod=color)
        self.char = char

        # perform a move to set up the initial position
        tile_size = self.scene.manager.tile_size
        self.sprite.move_ip(x * tile_size, y * tile_size)

    def move(self, dx, dy):
        """Move by the given amount.

        Args:
            dx (int): horizontal grid-relative distance
            dy (int): vertical grid-relative distance
        """
        tile_size = self.scene.manager.tile_size
        self.sprite.move_ip(dx * tile_size, dy * tile_size)

    def render(self):
        """Render the sprite to the buffer."""
        self.sprite.set_alpha_mod()
        self.sprite.set_color_mod()
        self.scene.spriterenderer.render(self.sprite)


if __name__ == '__main__':
    m = manager.Manager()
    m.set_scene(SceneRogueLike)
    m.run()

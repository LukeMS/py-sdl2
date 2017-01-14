"""A roguelike implementation."""

import sdl2
from sdl2.ext import manager


class SceneRogueLike(manager.SceneBase):
    """A roguelike game scene."""

    def __init__(self, **kwargs):
        """Initialization."""
        # create a character using the factory
        self.at = self.factory.get_char_sprite("@")
        # change its position
        self.at.move_ip(self.width // 2, self.height // 2)

    def on_update(self):
        """Graphical logic."""
        # render it
        self.spriterenderer.render(sprites=self.at)

    def on_key_release(self, event, sym, mod):
        """Called on keyboard input, when a key is **released**."""
        k = self.manager.tile_size
        if sym == sdl2.SDLK_ESCAPE:
            self.quit()
        elif sym == sdl2.SDLK_DOWN:
            self.at.move_ip(0, k)
        elif sym == sdl2.SDLK_UP:
            self.at.move_ip(0, -k)
        elif sym == sdl2.SDLK_RIGHT:
            self.at.move_ip(k, 0)
        elif sym == sdl2.SDLK_LEFT:
            self.at.move_ip(-k, 0)


if __name__ == '__main__':
    m = manager.Manager()
    m.set_scene(SceneRogueLike)
    m.run()

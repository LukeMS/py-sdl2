"""Animated sprite example."""


from sdl2.ext import Manager, SceneBase


class SceneAnimatedSprite(SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        self.sprite = self.factory.get_char_sprite("0")
        tile_size = self.factory._tile_size
        self.sprite.set_animation(10, 1, tile_size, tile_size)
        self.sprite.position = 128, 128

    def on_update(self):
        """..."""
        self.sprite.step(col=1)
        self.spriterenderer.render(sprites=self.sprite)


if __name__ == '__main__':
    m = Manager()
    m.set_scene(SceneAnimatedSprite)
    m.run()

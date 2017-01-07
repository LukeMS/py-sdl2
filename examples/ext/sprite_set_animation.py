"""Animated sprite example."""


from sdl2.ext import Manager, SceneBase


class SceneAnimatedSprite(SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        tile_size = self.factory._tile_size

        number = self.factory.get_char_sprite("0")
        number.set_animation(10, 1, tile_size, tile_size)
        number.topleft = 128, 128
        child = number.subsprite(area=number.frame_rect)
        child.set_animation(1, 2, tile_size, tile_size)
        child.topleft = number.move(32, 32).topleft
        self.sprites = [number, child]

    def on_update(self):
        """..."""
        [sprite.step(row=1, col=1) for sprite in self.sprites]
        self.spriterenderer.render(sprites=self.sprites)


if __name__ == '__main__':
    m = Manager()
    m.set_scene(SceneAnimatedSprite)
    m.run()

"""Create some sprites with rectangular forms and render them."""

from sdl2.ext.rect import Rect
from sdl2.ext.manager import Manager, SceneBase


class SceneRects(SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        from_color = self.manager.factory.from_color

        colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255)]

        rect_a = Rect(600, 10, 100, 100)
        rect_b = Rect(400, 400, 100, 100)
        rect_c = rect_a.gap(rect_b)

        self.sprites = {from_color(color=c, rect=r)
                        for c, r in zip(colors, [rect_a, rect_b, rect_c])}

    def on_update(self):
        """..."""
        super().on_update()
        self.manager.spriterenderer.render(sprites=self.sprites)

if __name__ == '__main__':
    m = Manager()
    m.set_scene(SceneRects)
    m.run()

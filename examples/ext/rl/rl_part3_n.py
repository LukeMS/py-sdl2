"""A roguelike implementation."""

from itertools import product

import sdl2
from sdl2.ext import manager

MAP_WIDTH = 40
MAP_HEIGHT = 22


class SceneRogueLike(manager.SceneBase):
    """A roguelike game scene."""

    ignore_regular_update = False

    def __init__(self, **kwargs):
        """Initialization."""
        # create a character using the factory
        self.player = GameObject(self, 8, 8, '@', (255, 255, 255, 255))
        npc = GameObject(self, 4, 4, '@', (255, 255, 0, 255))
        self.map = Map(MAP_WIDTH, MAP_HEIGHT)
        self.obj_factory = ObjectsFactory(self)
        [self.obj_factory.create_tile(x, y, "floor")
         for x in range(MAP_WIDTH)
         for y in range(MAP_HEIGHT)]
        # print(self.map)
        self.objects = [self.map, self.player, npc]

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


class Map(object):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.grid = [[Cell(x, y) for y in range(h)] for x in range(w)]

    def keys(self):
        return product(range(self.w), range(self.h))

    def values(self):
        for _v in self.grid:
            for v in _v:
                yield v

    def items(self):
        for x, _v in enumerate(self.grid):
            for y, v in enumerate(_v):
                yield ((x, y), v)

    def render(self):
        [cell.render() for cell in self.values()]

    def __getitem__(self, key):
        """Interface function for the internal grid.

        Args:
            key (tuple): 2 int tuple with x and y coordinates.
        Returns:
            Cell
        """
        x, y = key
        return self.grid[x][y]

    def __repr__(self):
        from pprint import pformat
        return pformat({k: v for k, v in self.items()}, indent=4)


class Cell(object):
    """A cell of the map, its properties and entities."""

    __slots__ = ("x", "y", "tile", "feature", "creature", "items")

    def __init__(
        self, x, y, tile=None, feature=None, creature=None, items=None
    ):
        """Initialization."""
        self.x = x
        self.y = y
        self.tile = tile
        self.feature = feature
        self.creature = creature
        self.items = items

    def render(self):
        objs = [obj for obj in (self.tile, self.feature, self.creature)
                if obj]
        if self.items:
            objs += self.items

        [obj.render() for obj in objs]

    def __repr__(self):
        pos = "(%d, %d)" % (self.x, self.y)
        tile = repr(self.tile)
        feature = repr(self.feature) if self.feature else None
        creature = repr(self.creature) if self.creature else None
        items = repr(self.items) if self.items else None

        return ", ".join(obj
                         for obj in [pos, tile, feature, creature, items]
                         if obj)


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

    def __repr__(self):
        return "%s(char=%s, sprite=%s)" % (
            self.__class__.__name__, self.char, self.sprite)


class ObjectsFactory(object):
    """Factory for game objects.

    Game entities can be creatures, items, features and tiles.
    """

    def __init__(self, scene):
        """Initialization.

        Args:
            scene (manager.SceneBase): instance of the running scene.
        """
        self.scene = scene

    def create_tile(self, x, y, tname):
        """Create a tile with the passed information.

        Args:
            tname (str): template name
        """
        block_sight = None
        if tname == "wall":
            block_move = True
            char = "#"
            color = (0, 0, 100)
        elif tname == "floor":
            block_move = False
            char = "."
            color = (50, 50, 150)
        block_sight = block_move if block_sight is None else block_sight
        block_move = block_move
        tile = GameObject(scene=self.scene, x=x, y=y, char=char, color=color)
        tile.block_sight = block_sight
        tile.block_move = block_move
        self.scene.map[x, y].tile = tile


if __name__ == '__main__':
    m = manager.Manager()
    m.set_scene(SceneRogueLike)
    m.run()

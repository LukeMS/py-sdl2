"""Sprite, texture and pixel surface routines.

Attributes:
    TEXTURE (int): Indicates that texture-based rendering or sprite creation
        is wanted.
    SOFTWARE (int): Indicates that software-based rendering or sprite
        creation is wanted.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from ctypes import byref, cast, POINTER, c_int, c_float, c_uint8
import warnings

from .. import blendmode, surface, rect, video, pixels, render, rwops
from ..stdinc import Uint8, Uint32
from ..util import iter_nested

from .common import SDLError
from .color import convert_to_color
from .ebs import System
from .surface import subsurface
from .window import Window, get_display_mode
from .image import load_image
from .rect import to_sdl_rect, NonIterableRect

__all__ = (
    "Sprite", "SoftwareSprite", "TextureSprite", "SpriteFactory",
    "SoftwareSpriteRenderSystem", "SpriteRenderSystem",
    "TextureSpriteRenderSystem", "Renderer", "TEXTURE", "SOFTWARE")

TEXTURE = 0
SOFTWARE = 1


class Renderer(object):
    """SDL2-based renderer for windows and sprites."""

    def __init__(
        self, target, index=-1, logical_size=None,
        flags=render.SDL_RENDERER_ACCELERATED
    ):
        """Create a new Renderer for the given target.

        If target is a Window or SDL_Window, index and flags are passed
        to the relevant sdl.render.create_renderer() call. If target is
        a SoftwareSprite or SDL_Surface, the index and flags arguments are
        ignored.
        """
        self.sdlrenderer = None
        self.rendertaget = None
        if isinstance(target, Window):
            self.sdlrenderer = render.SDL_CreateRenderer(target.window, index,
                                                         flags)
            self.rendertarget = target.window
        elif isinstance(target, video.SDL_Window):
            self.sdlrenderer = render.SDL_CreateRenderer(target, index, flags)
            self.rendertarget = target
        elif isinstance(target, SoftwareSprite):
            self.sdlrenderer = render.SDL_CreateSoftwareRenderer(
                target.surface)
            self.rendertarget = target.surface
        elif isinstance(target, surface.SDL_Surface):
            self.sdlrenderer = render.SDL_CreateSoftwareRenderer(target)
            self.rendertarget = target
        else:
            raise TypeError("unsupported target type")

        if logical_size is not None:
            self.logical_size = logical_size

    def __del__(self):
        """Destructor."""
        if self.sdlrenderer:
            render.SDL_DestroyRenderer(self.sdlrenderer)
        self.rendertarget = None

    @property
    def renderer(self):
        warnings.warn(
            "attribute renderer is deprecated, use sdlrenderer instead",
            DeprecationWarning)
        return self.sdlrenderer

    @property
    def logical_size(self):
        """The logical pixel size of the Renderer"""
        w, h = c_int(), c_int()
        render.SDL_RenderGetLogicalSize(self.sdlrenderer, byref(w), byref(h))
        return w.value, h.value

    @logical_size.setter
    def logical_size(self, size):
        """The logical pixel size of the Renderer"""
        width, height = size
        ret = render.SDL_RenderSetLogicalSize(self.sdlrenderer, width, height)
        if ret != 0:
            raise SDLError()

    @property
    def color(self):
        """The drawing color of the Renderer."""
        r, g, b, a = Uint8(), Uint8(), Uint8(), Uint8()
        ret = render.SDL_GetRenderDrawColor(self.sdlrenderer, byref(r), byref(g),
                                            byref(b), byref(a))
        if ret == -1:
            raise SDLError()
        return convert_to_color((r.value, g.value, b.value, a.value))

    @color.setter
    def color(self, value):
        """The drawing color of the Renderer."""
        c = convert_to_color(value)
        ret = render.SDL_SetRenderDrawColor(self.sdlrenderer, c.r, c.g, c.b, c.a)
        if ret == -1:
            raise SDLError()

    @property
    def blendmode(self):
        """The blend mode used for drawing operations (fill and line)."""
        mode = blendmode.SDL_BlendMode()
        ret = render.SDL_GetRenderDrawBlendMode(self.sdlrenderer, byref(mode))
        if ret == -1:
            raise SDLError()
        return mode

    @blendmode.setter
    def blendmode(self, value):
        """The blend mode used for drawing operations (fill and line)."""
        ret = render.SDL_SetRenderDrawBlendMode(self.sdlrenderer, value)
        if ret == -1:
            raise SDLError()

    @property
    def scale(self):
        """The horizontal and vertical drawing scale."""
        sx = c_float(0.0)
        sy = c_float(0.0)
        render.SDL_RenderGetScale(self.sdlrenderer, byref(sx), byref(sy))
        return sx.value, sy.value

    @scale.setter
    def scale(self, value):
        """The horizontal and vertical drawing scale."""
        ret = render.SDL_RenderSetScale(self.sdlrenderer, value[0], value[1])
        if ret != 0:
            raise SDLError()

    def clear(self, color=None):
        """Clears the renderer with the currently set or passed color."""
        if color is not None:
            tmp = self.color
            self.color = color
        ret = render.SDL_RenderClear(self.sdlrenderer)
        if color is not None:
            self.color = tmp
        if ret == -1:
            raise SDLError()

    def copy(
        self, src, srcrect=None, dstrect=None, angle=0, center=None,
        flip=render.SDL_FLIP_NONE
    ):
        """Copy (blit) the passed source to the target of the Renderer.

        Args:
            src (TextureSprite, sdl2.SDL_Texture): source to be copied

        Kwargs:
            srcrect (rect): rectangle to be used for clipping portions of src
            dstrect (rect): destination rectangle, where to blit
            angle (float): rotate around center by the given degrees

        Raises:
            TypeError, SDLError

        Example:
            >>> copy(src=tileset, srcrect=(0, 0, 32, 32),
                     dstrect=(128, 64, 32, 32))
        """

        if isinstance(src, TextureSprite):
            texture = src.texture
            angle = angle or src.angle
            center = (center or src.sdl_center)
            flip = flip or src.flip
        elif isinstance(src, render.SDL_Texture):
            texture = src
        else:
            raise TypeError("src must be a TextureSprite or SDL_Texture")
        if srcrect is not None:
            x, y, w, h = srcrect
            srcrect = rect.SDL_Rect(x, y, w, h)
        if dstrect is not None:
            x, y, w, h = dstrect
            dstrect = rect.SDL_Rect(x, y, w, h)
        ret = render.SDL_RenderCopyEx(self.sdlrenderer, texture, srcrect,
                                      dstrect, angle, center, flip)
        if ret == -1:
            raise SDLError()

    def present(self):
        """Refreshes the target of the Renderer."""
        render.SDL_RenderPresent(self.sdlrenderer)

    def draw_line(self, points, color=None):
        """Draws one or multiple connected lines on the renderer."""
        # (x1, y1, x2, y2, ...)
        pcount = len(points)
        if (pcount % 2) != 0:
            raise ValueError("points does not contain a valid set of points")
        if pcount < 4:
            raise ValueError("points must contain more that one point")
        if pcount == 4:
            if color is not None:
                tmp = self.color
                self.color = color
            x1, y1, x2, y2 = points
            ret = render.SDL_RenderDrawLine(self.sdlrenderer, x1, y1, x2, y2)
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            off = 0
            count = pcount // 2
            SDL_Point = rect.SDL_Point
            ptlist = (SDL_Point * count)()
            while x < pcount:
                ptlist[off] = SDL_Point(points[x], points[x + 1])
                x += 2
                off += 1
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(ptlist, POINTER(SDL_Point))
            ret = render.SDL_RenderDrawLines(self.sdlrenderer, ptr, count)
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()

    def draw_point(self, points, color=None):
        """Draws one or multiple points on the renderer."""
        # (x1, y1, x2, y2, ...)
        pcount = len(points)
        if (pcount % 2) != 0:
            raise ValueError("points does not contain a valid set of points")
        if pcount == 2:
            if color is not None:
                tmp = self.color
                self.color = color
            ret = render.SDL_RenderDrawPoint(self.sdlrenderer, points[0],
                                             points[1])
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            off = 0
            count = pcount // 2
            SDL_Point = rect.SDL_Point
            ptlist = (SDL_Point * count)()
            while x < pcount:
                ptlist[off] = SDL_Point(points[x], points[x + 1])
                x += 2
                off += 1
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(ptlist, POINTER(SDL_Point))
            ret = render.SDL_RenderDrawPoints(self.sdlrenderer, ptr, count)
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()

    def draw_rect(self, rects, color=None):
        """Draws one or multiple rectangles on the renderer."""
        SDL_Rect = rect.SDL_Rect
        # ((x, y, w, h), ...)
        if type(rects[0]) == int:
            # single rect
            if color is not None:
                tmp = self.color
                self.color = color
            x, y, w, h = rects
            ret = render.SDL_RenderDrawRect(
                self.sdlrenderer, SDL_Rect(x, y, w, h))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            rects = list(iter_nested(rects))
            rlist = (SDL_Rect * len(rects))()
            for idx, r in enumerate(rects):
                rlist[idx] = SDL_Rect(*r)
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(rlist, POINTER(SDL_Rect))
            ret = render.SDL_RenderDrawRects(self.sdlrenderer, ptr, len(rects))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()

    def fill(self, rects, color=None):
        """Fills one or multiple rectangular areas on the renderer."""
        SDL_Rect = rect.SDL_Rect
        # ((x, y, w, h), ...)
        if type(rects[0]) == int:
            # single rect
            if color is not None:
                tmp = self.color
                self.color = color
            x, y, w, h = rects
            ret = render.SDL_RenderFillRect(
                self.sdlrenderer, SDL_Rect(x, y, w, h))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            rects = list(iter_nested(rects))
            rlist = (SDL_Rect * len(rects))()
            for idx, r in enumerate(rects):
                rlist[idx] = SDL_Rect(*r)
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(rlist, POINTER(SDL_Rect))
            ret = render.SDL_RenderFillRects(self.sdlrenderer, ptr, len(rects))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()


class Sprite(NonIterableRect):
    """A simple 2D object, implemented as abstract base class."""

    _frame_rect = None
    _pixel_data = None

    def __init__(self, data, w, h, free):
        """Create a new sprite.

        Attributes:
            depth (int): The layer depth on which to draw the sprite.
                Objects with higher `depth` values will be drawn on top of
                other sprites by the :class:`SpriteRenderSystem`.
        """
        super().__init__(0, 0, w, h)
        self.depth = 0
        self._pixel_data = data
        self.free = free

    @property
    def frame_rect(self):
        """:attr: `frame_rect`."""
        return self._frame_rect

    @frame_rect.setter
    def frame_rect(self, val):
        self._frame_rect = to_sdl_rect(val) if val else None

    @property
    def area(self):
        """The rectangular area occupied by the sprite."""
        return tuple((p
                      for pos in (self.topleft, self.bottomright)
                      for p in pos))

    @property
    def position(self):
        """The top-left position of the Sprite as tuple."""
        # for compatibility with versions prior to 0.10
        return self.topleft

    @position.setter
    def position(self, value):
        """The top-left position of the Sprite as tuple."""
        # for compatibility with versions prior to 0.10
        self.topleft = value

    def __del__(self):
        """Release the bound `SDL_Surface`.

        Only if :attr:`sdl2.ext.sprite.SoftwareSprite.free` is `True`.
        """
        pixel_data = self._pixel_data
        if getattr(self, "free", None) and pixel_data is not None:
            self._releaser(pixel_data)
        self._pixel_data = None

    def __repr__(self):
        return "%s(area=%s)" % (self.__class__.__name__, self.area)


class SoftwareSprite(Sprite):
    """A simple, visible, pixel-based 2D object using software surfaces."""

    _releaser = surface.SDL_FreeSurface

    def __init__(self, imgsurface, free=True, area=None):
        """Create a new SoftwareSprite.

        Args:
            imgsurface (`sdl2.SDL_Surface`): the surface containing pixel data
                for this sprite.
            free (bool): when set to `True` the surface is released when the
                sprite is deleted/garbage collected.
        """
        if not isinstance(imgsurface, surface.SDL_Surface):
            raise TypeError("surface must be a SDL_Surface")
        if area:
            w, h = NonIterableRect(area).size
        else:
            w, h = imgsurface.w, imgsurface.h
        super().__init__(imgsurface, w, h, free)

    @property
    def surface(self):
        """`sdl2.SDL_Surface` containing pixel data."""
        return self._pixel_data

    def subsprite(self, area):
        """Create another `SoftwareSprite` from part of the sprite's surface.

        The two sprites share pixel data, so if the parent sprite's surface is
        not managed by the sprite (``free`` is False), you will need to keep
        it alive while the subsprite exists.

        Args:
            area (tuple): x, y, w, h (position and size) of the area,
                in pixels.

        Returns:
            SoftwareSprite
        """
        ssurface = subsurface(self.surface, area)
        ssprite = SoftwareSprite(ssurface, True)
        # Keeps the parent surface alive until subsprite is freed
        if self.free:
            ssprite._parent = self
        return ssprite


class TextureSprite(Sprite):
    """A simple, visible, texture-based 2D object, using a renderer."""

    _releaser = render.SDL_DestroyTexture
    alpha_mod = None
    color_mod = None

    def __init__(self, texture, free=True, area=None, **kwargs):
        """Create a new TextureSprite.

        Args:
            texture (sdl2.SDL_Texture): the texture containing the sprite
                pixel data.
            free (bool): when set to `True` the texture is released when the
                sprite is deleted/garbage collected.
            kwargs (dict): additional kwargs are unpacked to the instance
                __dict__ before processing the other arguments.

        Attributes:
            angle (int): The rotation angle for the :class:`TextureSprite`.
            flip (sdl2.SDL_FLIP_NONE, sdl2.SDL_FLIP_HORIZONTAL,
                sdl2.SDL_FLIP_VERTICAL): Allows the `TextureSprite` to be
                flipped over its horizontal or vertical axis via the
                appropriate SDL_FLIP_* value.
            texture (sdl2.SDL_Texture): the texture containing the sprite
                pixel data.
            color_mod (tuple): 3 rgb color int values between 0 and 255,
                the default color_mod for this sprite.
            alpha_mod (int): integer between 0 and 255, the default alpha_mod
                for this sprite.
        """
        self.__dict__.update(kwargs)
        self._pixel_data = texture
        if area:
            w, h = NonIterableRect(area).size
            super().__init__(texture, w, h, free)
            self.frame_rect = area
        else:
            flags = Uint32()
            access = c_int()
            w = c_int()
            h = c_int()
            ret = render.SDL_QueryTexture(
                texture, byref(flags), byref(access), byref(w), byref(h))
            if ret == -1:
                raise SDLError()
            super().__init__(texture, w.value, h.value, free)
        self.angle = 0.0
        self.flip = render.SDL_FLIP_NONE

    @property
    def texture(self):
        """`sdl2.SDL_Texture` containing pixel data."""
        return self._pixel_data

    def subsprite(self, area, **kwargs):
        """Create another sprite from part of this sprite's pixel data.

        The two sprites share pixel data, so if the parent sprite's surface is
        not managed by the sprite (``free`` is False), you will need to keep
        it alive while the subsprite exists.

        Args:
            area (tuple): x, y, w, h (position and size) of the area,
                in pixels.
            kwargs (dict): additional kwargs are passed forward to the
                TextureSprite initialization.

        Returns:
            TextureSprite
        """
        data = self._pixel_data
        return TextureSprite(data, False, area, **kwargs)

    @property
    def sdl_center(self):
        """The center of the TextureSprite as tuple."""
        return rect.SDL_Point(*self.center)

    def set_animation(self, cols, rows, col_w, row_h, col=0, row=0):
        """"Set animation frames parameters.

        Args:
            cols (int): number of frame columns
            rows (int): number of frame rows
            col_w (int): width of each column, in pixels
            row_h (int): height of each row, in pixels
            col (int): the column of the desired starting frame
            row (int): the row of the desired starting frame

        Returns:
            TextureSprite

                self instance, making it possible to use this method on the
                object creation (see Usage below) as a one liner.

        Example:
            Here a 10x1 area of 32x32 tiles is used:

                >>> sprite = TextureSprite(**kwargs).set_animation(
                        10, 1, 32, 32)
        """
        rect = self.frame_rect
        self.tile_offset_x = rect.x // col_w
        self.tile_offset_y = rect.y // row_h
        self.cols = cols
        self.rows = rows
        self.col_w = col_w
        self.row_h = row_h
        self.col = col
        self.row = row
        self._size = col_w, row_h
        self.set_current_rect()

        return self

    def set_current_rect(self):
        """Apply the current animation parameters to the frame_rect."""
        self.frame_rect = ((self.col + self.tile_offset_x) * self.col_w,
                           (self.row + self.tile_offset_y) * self.row_h,
                           self.col_w,
                           self.row_h)

    def step(self, col=0, row=0):
        """..."""
        if not col and not row:
            return
        if col:
            self.col += col
            self.col = self.col % self.cols
        if row:
            self.row += row
            self.row = self.row % self.rows
        self.set_current_rect()

    def get_alpha_mod(self):
        """Get the alpha value multiplier for render copy operations.

        This is the value currently set for the texture. If a texture is used
        by more then one sprite, the modifier as defined on its last copy
        operation will be returned.

        Returns:
            (int): integer alpha value.
        """
        alpha = c_uint8(0)
        render.SDL_GetTextureAlphaMod(self.texture, byref(alpha))
        return alpha.value

    def get_color_mod(self):
        """Get the color value multiplier for render copy operations.

        This is the value currently set for the texture. If a texture is used
        by more then one sprite, the modifier as defined on its last copy
        operation will be returned.

        Returns:
            (int), (int), (int): 3-tuple of rgb integer values (RGB).
        """
        r = c_uint8(0)
        g = c_uint8(0)
        b = c_uint8(0)
        if render.SDL_GetTextureAlphaMod(
                self.texture, byref(r), byref(g), byref(b)):
            raise SDLError()

        return r.value, g.value, b.value

    def set_alpha_mod(self, alpha=None):
        """Set a alpha value multiplier for render copy operations.

        When this texture is rendered, during the copy operation the source
        alpha value is modulated by this alpha value according to the
        following formula:
            srcA = srcA * (alpha / 255)

        Args:
            alpha (int): integer between 0 and 255
        """
        alpha = alpha or self.alpha_mod or 255
        if render.SDL_SetTextureAlphaMod(self.texture, alpha):
            raise SDLError()

    def set_color_mod(self, color=None):
        """Set a color value multiplier for render copy operations.

        When this texture is rendered, during the copy operation each source
        color channel is modulated by the appropriate color value according
        to the following formula:
            srcC = srcC * (color / 255)

        Args:
            color (3-tuple of ints): rgb color with values between 0 and 255
        """
        if isinstance(color, float):
            color = tuple(
                min(max(int(255 * color), 0), 255) for i in range(3))
        else:
            color = color or self.color_mod or (255, 255, 255)

        if render.SDL_SetTextureColorMod(self.texture, *color):
            raise SDLError()


class SpriteFactory(object):
    """A factory class for creating Sprite components."""

    def __init__(self, sprite_type=TEXTURE, **kwargs):
        """Creates a new SpriteFactory.

        The SpriteFactory can create TextureSprite or SoftwareSprite
        instances, depending on the sprite_type being passed to it,
        which can be SOFTWARE or TEXTURE. The additional kwargs are used
        as default arguments for creating sprites within the factory
        methods.
        """
        if sprite_type == TEXTURE:
            if "renderer" not in kwargs:
                raise ValueError("you have to provide a renderer=<arg> argument")
        elif sprite_type != SOFTWARE:
            raise ValueError("sprite_type must be TEXTURE or SOFTWARE")
        self._spritetype = sprite_type
        self.default_args = kwargs

    @property
    def sprite_type(self):
        """The sprite type created by the factory."""
        return self._spritetype

    def __repr__(self):
        stype = "TEXTURE"
        if self.sprite_type == SOFTWARE:
            stype = "SOFTWARE"
        return "SpriteFactory(sprite_type=%s, default_args=%s)" % \
            (stype, self.default_args)

    def create_sprite_render_system(self, *args, **kwargs):
        """Create a new SpriteRenderSystem.

        For TEXTURE mode, the passed args are ignored.
        The renderer can be passed as kwarg and defaults to the SDL_Renderer
        passed to the SpriteFactory during its creation.
        """
        if self.sprite_type == TEXTURE:
            default = self.default_args.copy()
            default.update(kwargs)
            target = default.pop("renderer")
            return TextureSpriteRenderSystem(target, **default)
        else:
            return SoftwareSpriteRenderSystem(*args, **kwargs)

    def load_tileset(self, sprite, tile_size):
        """..."""
        self._tileset = sprite
        self._tileset_w, self._tileset_h = self._tileset.size
        self._tile_size = tile_size

    def get_char_sprite(self, char, **kwargs):
        """Get the passed character from the current tileset, as a sprite.

        Args:
            char (str): string of one character to be rendered
            kwargs (dict): additional kwargs are passed forward to the
                subsprite functione of the tileset sprite.
        """
        _id = ord(char)
        tile_size = self._tile_size
        row = _id // (self._tileset_w // tile_size)
        col = _id % (self._tileset_w // tile_size)
        area = (col * tile_size, row * tile_size, tile_size, tile_size)
        return self._tileset.subsprite(area, **kwargs)

    def from_image(self, fname):
        """Create a Sprite from the passed image file."""
        return self.from_surface(load_image(fname), True)

    def from_surface(self, tsurface, free=False):
        """Create a Sprite from the passed SDL_Surface.

        If free is set to True, the passed surface will be freed
        automatically.
        """
        if self.sprite_type == TEXTURE:
            renderer = self.default_args["renderer"]
            texture = render.SDL_CreateTextureFromSurface(renderer.sdlrenderer,
                                                          tsurface)
            if not texture:
                raise SDLError()
            sprite = TextureSprite(texture.contents)
            if free:
                surface.SDL_FreeSurface(tsurface)
            return sprite
        elif self.sprite_type == SOFTWARE:
            return SoftwareSprite(tsurface, free)
        raise ValueError("sprite_type must be TEXTURE or SOFTWARE")

    def from_object(self, obj):
        """Create a Sprite from an arbitrary object."""
        if self.sprite_type == TEXTURE:
            rw = rwops.rw_from_object(obj)
            # TODO: support arbitrary objects.
            imgsurface = surface.SDL_LoadBMP_RW(rw, True)
            if not imgsurface:
                raise SDLError()
            return self.from_surface(imgsurface.contents, True)
        elif self.sprite_type == SOFTWARE:
            rw = rwops.rw_from_object(obj)
            imgsurface = surface.SDL_LoadBMP_RW(rw, True)
            if not imgsurface:
                raise SDLError()
            return SoftwareSprite(imgsurface.contents, True)
        raise ValueError("sprite_type must be TEXTURE or SOFTWARE")

    def from_color(
        self, color, size=None, bpp=32, masks=None, pos=None, rect=None
    ):
        """Create a sprite with a certain color.

        Either `size` or `rect` is required.
        A :class:`sdl.SDL_Surface` is first created and then a sprite is
        created passing it as parameter, using :func: `from_surface`.

        Args:
            color (:class: `sdl2.ext.color.Color`, tuple): color of the
                sprite to be created. Can be a Color or a tuple of 3-4 int
                (RGB or RGBA).
            size (tuple): size (int width, int height) of the sprite to be
                created, in pixels.
            bpp (int): the depth of the sprite's surface, in bits

        Raises:
            ValueError if neither size or rect arguments are passed
            SDLError if an error occurs during the  creation of the surface

        """
        if rect:
            rect = NonIterableRect(rect)
            pos, size = rect.topleft, rect.size
        else:
            if size is None:
                raise ValueError("invalid size")
            if pos is None:
                pos = (0, 0)

        color = convert_to_color(color)
        if masks:
            rmask, gmask, bmask, amask = masks
        else:
            rmask = gmask = bmask = amask = 0
        sfc = surface.SDL_CreateRGBSurface(0, size[0], size[1], bpp, rmask,
                                           gmask, bmask, amask)
        if not sfc:
            raise SDLError()
        sfc = sfc.contents
        fmt = sfc.format.contents
        if fmt.Amask != 0:
            # Target has an alpha mask
            col = pixels.SDL_MapRGBA(fmt, color.r, color.g, color.b, color.a)
        else:
            col = pixels.SDL_MapRGB(fmt, color.r, color.g, color.b)
        ret = surface.SDL_FillRect(sfc, None, col)
        if ret == -1:
            raise SDLError()
        sprite = self.from_surface(sfc, True)
        sprite.position = pos
        return sprite

    def from_text(self, text, **kwargs):
        """Creates a Sprite from a string of text."""
        args = self.default_args.copy()
        args.update(kwargs)
        fontmanager = args['fontmanager']
        sfc = fontmanager.render(text, **args)
        return self.from_surface(sfc, free=True)

    def create_sprite(self, **kwargs):
        """Creates an empty Sprite.

        This will invoke create_software_sprite() or
        create_texture_sprite() with the passed arguments and the set
        default arguments.
        """
        args = self.default_args.copy()
        args.update(kwargs)
        if self.sprite_type == TEXTURE:
            return self.create_texture_sprite(**args)
        else:
            return self.create_software_sprite(**args)

    def create_software_sprite(self, size, bpp=32, masks=None):
        """Creates a software sprite.

        A size tuple containing the width and height of the sprite and a
        bpp value, indicating the bits per pixel to be used, need to be
        provided.
        """
        if masks:
            rmask, gmask, bmask, amask = masks
        else:
            rmask = gmask = bmask = amask = 0
        imgsurface = surface.SDL_CreateRGBSurface(0, size[0], size[1], bpp,
                                                  rmask, gmask, bmask, amask)
        if not imgsurface:
            raise SDLError()
        return SoftwareSprite(imgsurface.contents, True)

    def create_texture_sprite(self, renderer, size,
                              pformat=pixels.SDL_PIXELFORMAT_RGBA8888,
                              access=render.SDL_TEXTUREACCESS_STATIC):
        """Creates a texture sprite.

        A size tuple containing the width and height of the sprite needs
        to be provided.

        TextureSprite objects are assumed to be static by default,
        making it impossible to access their pixel buffer in favour for
        faster copy operations. If you need to update the pixel data
        frequently or want to use the texture as target for rendering
        operations, access can be set to the relevant
        SDL_TEXTUREACCESS_* flag.
        """
        if isinstance(renderer, render.SDL_Renderer):
            sdlrenderer = renderer
        elif isinstance(renderer, Renderer):
            sdlrenderer = renderer.sdlrenderer
        else:
            raise TypeError("renderer must be a Renderer or SDL_Renderer")
        texture = render.SDL_CreateTexture(sdlrenderer, pformat, access,
                                           size[0], size[1])
        if not texture:
            raise SDLError()
        return TextureSprite(texture.contents)


class SpriteRenderSystem(System):
    """A rendering system for Sprite components.

    This is a base class for rendering systems capable of drawing and
    displaying Sprite-based objects. Inheriting classes need to
    implement the rendering capability by overriding the render()
    method.
    """
    def __init__(self):
        super(SpriteRenderSystem, self).__init__()
        self.componenttypes = (Sprite,)
        self._sortfunc = lambda e: e.depth

    def render(self, sprites, x=None, y=None):
        """Renders the passed sprites.

        This is a no-op function and needs to be implemented by inheriting
        classes.
        """
        pass

    def process(self, world, components):
        """Draws the passed SoftSprite objects on the Window's surface."""
        self.render(sorted(components, key=self._sortfunc))

    @property
    def sortfunc(self):
        """Sort function for the component processing order.

        The default sort order is based on the depth attribute of every
        sprite. Lower depth values will cause sprites to be drawn below
        sprites with higher depth values.
        """
        return self._sortfunc

    @sortfunc.setter
    def sortfunc(self, value):
        """Sort function for the component processing order.

        The default sort order is based on the depth attribute of every
        sprite. Lower depth values will cause sprites to be drawn below
        sprites with higher depth values.
        """
        if not callable(value):
            raise TypeError("sortfunc must be callable")
        self._sortfunc = value


class SoftwareSpriteRenderSystem(SpriteRenderSystem):
    """A rendering system for SoftwareSprite components.

    The SoftwareSpriteRenderSystem class uses a Window as drawing device to
    display Sprite surfaces. It uses the Window's internal SDL surface as
    drawing context, so that GL operations, such as texture handling or
    using SDL renderers is not possible.
    """
    def __init__(self, window):
        """Creates a new SoftwareSpriteRenderSystem for a specific Window."""
        super(SoftwareSpriteRenderSystem, self).__init__()
        if isinstance(window, Window):
            self.window = window.window
        elif isinstance(window, video.SDL_Window):
            self.window = window
        else:
            raise TypeError("unsupported window type")
        sfc = video.SDL_GetWindowSurface(self.window)
        if not sfc:
            raise SDLError()
        self.surface = sfc.contents
        self.componenttypes = (SoftwareSprite,)

    def render(self, sprites, x=None, y=None):
        """Draws the passed sprites (or sprite) on the Window's surface.

        x and y are optional arguments that can be used as relative drawing
        location for sprites. If set to None, the location information of the
        sprites are used. If set and sprites is an iterable, such as a list of
        SoftwareSprite objects, x and y are relative location values that will
        be added to each individual sprite's position. If sprites is a single
        SoftwareSprite, x and y denote the absolute position of the
        SoftwareSprite, if set.
        """
        r = rect.SDL_Rect(0, 0, 0, 0)
        try:
            _iter = (sprite for sprite in sprites)
            blit_surface = surface.SDL_BlitSurface
            imgsurface = self.surface
            x = x or 0
            y = y or 0
            for sprite in _iter:
                r.x = x + sprite.x
                r.y = y + sprite.y
                # get the frame_rect of a sprite if it has one
                frame_rect = sprite.frame_rect or None
                # pass the frame_rect as argument instead of None
                blit_surface(sprite.surface, frame_rect, imgsurface, r)
        except TypeError:
            r.x = sprites.x
            r.y = sprites.y
            if x is not None and y is not None:
                r.x = x
                r.y = y
                # get the frame_rect of a sprite if it has one
            frame_rect = sprites.frame_rect or None
                # pass the frame_rect as argument instead of None
            surface.SDL_BlitSurface(
                sprites.surface, frame_rect, self.surface, r)
        video.SDL_UpdateWindowSurface(self.window)


class TextureSpriteRenderSystem(SpriteRenderSystem):
    """A rendering system for TextureSprite components.

    The TextureSpriteRenderSystem class uses a SDL_Renderer as drawing
    device to display TextureSprite objects.
    """
    def __init__(self, target, present=True, *args, **kwargs):
        """Creates a new TextureSpriteRenderSystem.

        target can be a Window, SDL_Window, Renderer or SDL_Renderer.
        If it is a Window or SDL_Window instance, a Renderer will be
        created to acquire the SDL_Renderer.
        """
        super(TextureSpriteRenderSystem, self).__init__()
        if isinstance(target, (Window, video.SDL_Window)):
            # Create a Renderer for the window and use that one.
            target = Renderer(target)
        if isinstance(target, Renderer):
            self._renderer = target  # Used to prevent GC
            sdlrenderer = target.sdlrenderer
        elif isinstance(target, render.SDL_Renderer):
            sdlrenderer = target
        else:
            raise TypeError("unsupported object type")
        self.sdlrenderer = sdlrenderer
        self.componenttypes = (TextureSprite,)
        self.present = present
        self.max_x, self.max_y = get_display_mode()

    def render(self, sprites, x=None, y=None, present=None):
        """Draw the passed sprites (or sprite).

        Args:
            sprites (sdl2.ext.sprite.Sprite, iterable): the sprite(s) to be
                rendered.
            x (int): if None, the sprites position will be used; if not None
                and `sprites` is an iterable, it will be considered as a
                relative  position, added to the sprite position; if not None
                and sprites is a single sprite, will be considered as absolute
                position.
            y (int): same as x, for vertical position.
            present (bool): if True the rendered data will be presented at the
                end of the method. Defaults to None.

        Raises:
            SDLError (if sdl2.render.SDL_RenderCopyEx fails)
        """
        def out_of_bounds(r):
            return ((r.x + r.w) > self.max_x) or ((r.y + r.h) > self.max_y)

        r = rect.SDL_Rect(0, 0, 0, 0)
        rcopy = render.SDL_RenderCopyEx

        try:
            _iter = (sprite for sprite in sprites)
            renderer = self.sdlrenderer
            x = x or 0
            y = y or 0
            for sprite in _iter:
                r.x = x + sprite.x
                r.y = y + sprite.y
                r.w, r.h = sprite.size
                # get the frame_rect of a sprite if it has one
                frame_rect = sprite.frame_rect or None
                # pass the frame_rect as argument instead of None
                if out_of_bounds(r):
                    continue
                if rcopy(
                    renderer, sprite.texture, frame_rect, r, sprite.angle,
                    sprite.sdl_center, sprite.flip
                ) == -1:
                    raise SDLError()
        except TypeError:
            r.x = sprites.x
            r.y = sprites.y
            r.w, r.h = sprites.size
            if x is not None and y is not None:
                r.x = x
                r.y = y
            # get the frame_rect of a sprite if it has one
            frame_rect = sprites.frame_rect or None
            # pass the frame_rect as argument instead of None
            if out_of_bounds(r):
                return
            if rcopy(
                self.sdlrenderer, sprites.texture, frame_rect, r,
                sprites.angle, sprites.sdl_center, sprites.flip
            ) == -1:
                raise SDLError()
        if present is False:
            # Explicitly asked not to render
            return
        elif present or self.present:
            render.SDL_RenderPresent(self.sdlrenderer)

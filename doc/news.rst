Release News
============
This describes the latest changes between the PySDL2 releases.


----

0.10.0
------------
Released on 2017-01-06

* :mod:`sdl2.ext.manager` |new|

  - provides a basic scene manager (:class:`sdl2.ext.manager.Manager`) and a basic scene (:class:`sdl2.ext.manager.SceneBase`). The goal here is provide pysdl2 with a minimal engine, high level over sdl2.ext high level.

* :mod:`sdl2.ext.rect` |new|

  - provides a rectangular object implementation to facilitate coordinates storage and manipulation (:class:`sdl2.ext.rect.Rect`)


* :mod:`sdl2.ext.time` |new|

  - added :mod:`sdl2.ext.time`, providing a  high level interface to handle time and framerate.

* :mod:`sdl2.util` |new|

  - a config file parser (:func:`sdl2.util.get_cfg`);
  - a path utility (:func:`sdl2.util.sdl2_path`);
  - a singleton metaclass (:class:`sdl2.util.Singleton`)

* :mod:`sdl2.ext.sprite`

    * doens't free/delete its texture when deleted;
    * makes use of the :func:`sdl2.ext.sprite.Sprite.frame_rect` property to store a logical sub-area of the texture to be rendered.

  - :class:`sdl2.ext.sprite.Sprite`

    * It is now a subclass of :class:`sdl2.ext.rect.Rect`.
    * Sprites can now be manipulated as a Rect and have all of its properties.
    * See :mod:`sdl2.ext.rect` for more information on Rect and related.

  - :class:`sdl2.ext.sprite.TextureSpriteRenderSystem`

    * added optional parameter at initialization: `present`. By default it is set to `True` (same behavior as previously). If set to `False` during initialization of the sprite renderer, when :func:`sdl2.ext.sprite.TextureSpriteRenderSystem.render` is used with default parameters, it will no longer present what was rendered to the screen at the end. With that it is now possible to call render more then once without incurring in multiple `present` calls. The :class:`Manager` makes use of that so that it can call `present` only once, at the end of its loop.
    * :func:`sdl2.ext.sprite.TextureSpriteRenderSystem.render` also takes an optional `present` argument so that its behavior can be changed directly when calling `render`: if passed as `True` it will present at the end; if passed as `False` it will not present at the end, even if the default behavior passed during initialization is set to `True`.
    * Those should give total control of whether to present or not and when to do it while also keeping compatibility with prior versions.

  - :class:`sdl2.ext.sprite.SpriteFactory`

    * :func:`sdl2.ext.sprite.SpriteFactory.load_tileset` |new|

      - load a default tileset on the factory so that it can be used later on

    * :func:`sdl2.ext.sprite.SpriteFactory.get_char_sprite` |new|

      - create a character sprite from a tileset (bitmap font)

  - :class:`sdl2.ext.sprite.TextureSprite`

    * :func:`sdl2.ext.sprite.TextureSprite.__init__`

      - added optional parameter `free`. When set to True (default behavior for this and prior versions), on destruction/garbage colleting of the sprite, the texture will be destroyed. When set to False, the texture will be kept.
        This is useful for TextureSprite's that share a texture, such as a tileset.

    * :func:`sdl2.ext.sprite.TextureSprite.set_animation` |new|

      - set parameters for a animated (multi-framed) sprite

    * :func:`sdl2.ext.sprite.TextureSprite.step` |new|

      - step `n` rows or columns according to the animation parameters previously defined, wrapping it to respect its boundaries

    * :func:`sdl2.ext.sprite.TextureSprite.subsprite` |new|

      - create a TextureSprite from the same texture of the sprite, sharing it, considering an area of it to be used when rendering.

* :mod:`sdl2.dll`, :mod:`sdl2.sdlgfx`, :mod:`sdl2.sdlimage`, :mod:`sdl2.sdlmixer`, :mod:`sdl2.sdlttf`

  - using the config parser to read `PYSDL2_DLL_PATH` from `sdl2/sdl2.cfg` when the OS environment variable is not defined:

    >>> os.environ.setdefault("PYSDL2_DLL_PATH", get_cfg('DLL', 'PYSDL2_DLL_PATH'))

  - the OS enviroment variable takes precedence, so that it can still be defined on the OS enviroment or on a per-project base, as usual, as described on :ref:`importing-pysdl2`


* updated/modified documentation to use more of sphinx auto* tools, mostly on the API reference. The goal here was to remove text from .rst files that could be used as docstrings on the source code, making it easier to keep the documentation up to date with changes.


----

0.9.5
------------
Released on 2016-10-20.

* updated :mod:`sdl2` to include the latest changes of SDL2 (release 2.0.5)
* fixed issue #94: added support for TrueType font collection (TTC) files
* fixed issue #80: added flip and rotation support for TextureSprite objects
* renamed :attr:`sdl2.ext.Renderer.renderer` attribute to
  :attr:`sdl2.ext.Renderer.sdlrenderer`. The `renderer` attribute is
  deprecated and will be removed in a later version.

----

0.9.4
------------
Released on 2016-07-07.

* updated :mod:`sdl2` to include the latest changes of SDL2 (release 2.0.4)
* updated :mod:`sdl2.sdlttf` to include the latest changes of SDL_ttf (release 2.0.14)
* new :attr:`sdl2.ext.Renderer.logical_size` attribute to set or retrieve the logical
  pixel size of a renderer
* fixed issue #48: be more noisy about DLL loading issues
* fixed issue #65: misleading documentation for :meth:`sdl2.ext.Renderer.draw_line()`
* fixed issue #67: Return a proper error code, when unittests running as subprocesses fail
* fixed issue #72: :func:`sdl2.video.SDL_GL_DrawableSize()` not available on import
* fixed issue #76: define missing SDL_PRESSED and SDL_RELEASED constants
* fixed issue #82: examples/gui.py fails due to an attribute error
* fixed issue #83: fix compatibility with newer PIL versions in
  :func:`sdl2.ext.image.load_image()`
* fixed issue #84: The setter of :attr:`sdl2.ext.Renderer.scale` works properly now
* fixed issue #85: fix environment-dependent unit tests
* fixed issue #87: fix incorrect MIX_INIT_* constants in :mod:`sdl2.sdlmixer`
* fixed issue #88: use PILs `Image.tobyte()instead of the deprecated `Image.tostring()`
* fixed horizontical and vertical line drawing in :func:`sdl2.ext.line()`
* fixed a bug in :meth:`sdl2.ext.Renderer.draw_line()` for odd numbers of points
* dropped IronPython support

0.9.3
------------
Released on 2014-07-08.

* updated :mod:`sdl2` to include the latest changes of SDL2 (HG)
* new :attr:`sdl2.ext.Renderer.scale` attribute, which denotes the horizontal
  and vertical drawing scale
* new :func:`sdl2.ext.point_on_line()` function to test, if a point lies on a
  line segment
* PYSDL2_DLL_PATH can contain multiple paths separated by :attr:`os.pathsep`
  to search for the libraries now
* :func:`sdl2.ext.get_image_formats()` only returns BMP image support now, if
  SDL2_image and PIL are not found
* :func:`sdl2.ext.load_image()` tries to use :func:`sdl2.SDL_LoadBMP()` now,
  if SDL2_image and PIL are not found
* fixed issue #55: :meth:`sdl2.SDL_GameControllerAddMappingsFromFile()` does
  not raise a TypeError for Python 3.x anymore
* fixed issue #56: :meth:`sdl2.ext.Renderer.draw_line()` and
  :func:`sdl2.ext.Renderer.draw_point()` handle multiple lines (or points) as
  arguments properly now
* fixed issue #57: if SDL2_image is not installed and PIL is used, the loaded
  pixel buffer of the image file is not referenced anymore after returning
  from :func:`sdl2.ext.load_image()`, causing random segmentation faults
* fixed issue #58: raise a proper error,
  if :meth:`sdl2.ext.FontManager.render()` could not render a text surface
* fixed issue #59: The :attr:`sdl2.ext.TextureSpriteRenderSystem.sdlrenderer`
  attribute is correctly documented now
* fixed a local variable and module name collision in
  :meth:`sdl2.ext.FontManager.render()`

Thanks to Filip M. Nowak for the PYSDL2_DLL_PATH improvement.

0.9.2
------------
Released on 2014-04-13.

* fixed issue #32: the line clipping algorithms do not run into precision
  errors anymore
* fixed issue #53 (again): :func:`sdl2.video.SDL_GL_ResetAttributes()`
  is properly wrapped now to retain backwards compatibility with previous
  SDL2 releases
* fixed issue #54: text input is correctly converted for the text entry
  component
* updated the example BMP files, which could not be loaded properly on
  some systems with SDL2_image and PIL

0.9.1
------------
Released on 2014-04-05.

* fixed issue #50: corrected the :func:`sdl2.ext.load_image()`
  documentation
* fixed issue #52: :meth:`sdl2.ext.Renderer.fill()`,
  :meth:`sdl2.ext.Renderer.draw_rect()` and
  :meth:`sdl2.ext.Renderer.draw_point()` convert sequences
  correctly now
* fixed issue #53: provide backwards compatibility for previous
  SDL2 releases by adding a wrapper func for
  :func:`sdl2.cpuinfo.SDL_HasAVX()`

0.9.0
------------
Released on 2014-03-23.

**IMPORTANT: This release breaks backwards-compatibility. See the notes
for the issues #36 and #39.**

* updated :mod:`sdl2` to include the latest changes of SDL2 (release 2.0.3)
* new :func:`sdl2.ext.subsurface()` function to create subsurfaces from
  :class:`sdl2.SDL_Surface` objects
* new :func:`sdl2.ext.SoftwareSprite.subsprite()` method to create
  :class:`sdl2.ext.SoftwarSprite` objects sharing pixel data
* the unit test runner features a `--logfile` argument now to
  safe the unit test output to a file
* issues #36, #39: the different render classes of sdl2.ext.sprite were renamed

  * the ``sdl2.ext.RenderContext`` class was renamed to
    :class:`sdl2.ext.Renderer` to be consistent with with SDL2's naming scheme
  * ``sdl2.ext.SpriteRenderer`` was renamed to
    :class:`sdl2.ext.SpriteRenderSystem`
  * ``sdl2.ext.SoftwareSpriteRenderer`` was renamed to
    :class:`sdl2.ext.SoftwareSpriteRenderSystem`
  * ``sdl2.ext.TextureSpriteRenderer`` was renamed to
    :class:`sdl2.ext.TextureSpriteRenderSystem`
  * ``sdl2.ext.SpriteFactory.create_sprite_renderer()`` was renamed to
    :meth:`sdl2.ext.SpriteFactory.create_sprite_render_system()`

* fixed :func:`sdl2.audio.SDL_LoadWAV()` macro to provide the correct arguments
* fixed issue #44: use a slightly less confusing ``ValueError``, if a renderer
  argument for the :class:`sdl2.ext.SpriteFactory` is not provided
* fixed issue #43: improved the code reference for the improved bouncing
  section in the docs
* fixed issue #40: typo in a ``RuntimeWarning`` message on loading the SDL2
  libraries
* fixed issue #38: the points arguments of
  :meth:`sdl2.ext.Renderer.draw_points()` are properly documented now
* fixed issue #37: :func:`sdl2.SDL_GetRendererOutputSize()` is now acccessible
  via a wildcard import
* fixed issue #35: download location is now mentioned in the docs
* fixed issue #12: remove confusing try/except on import in the examples


0.8.0
------------
Released on 2013-12-30.

* updated PD information to include the CC0 dedication, since giving
  software away is not enough anymore
* updated :mod:`sdl2` to include the latest changes of SDL2 (HG)
* fixed a wrong C mapping of :func:`sdl2.rwops.SDL_FreeRW()`
* fixed various issues within the :class:`sdl2.ext.BitmapFont` class
* issue #26: :attr:`sdl2.SDL_AudioSpec.callback` is a :func:`SDL_AudioCallBack`
  now
* issue #30: the SDL_Add/DelHintCallback() unittest works with PyPy now
* issue #31: :func:`sdl2.sdlmixer.SDL_MIXER_VERSION()` returns the proper
  version now

Thanks to Sven Eckelmann, Marcel Rodrigues, Michael McCandless,
Andreas Schiefer and Franz Schrober for providing fixes and
improvements.

0.7.0
------------
Released on 2013-10-27.

* updated :mod:`sdl2` to include the latest changes of SDL2 (release 2.0.1)
* fixed a bug in :meth:`sdl2.ext.FontManager.render()`, which did not apply
  the text color correctly
* issue #14: improved the error messages on failing DLL imports
* issue #19: the :meth:`sdl2.ext.TextureSpriteRenderer.render()` and
  :meth:`sdl2.ext.SoftwareSpriteRenderer.render()` methods do not
  misinterpret x and y arguments anymore, if set to 0
* issue #21: :func:`sdl2.ext.load_image()` raises a proper
  :exc:`UnsupportedError`, if neither SDL_image nor PIL are usable

Thanks to Marcel Rodrigues, Roger Flores and otus for providing fixes
and improvement ideas.

0.6.0
------------
Released on 2013-09-01.

* new :attr:`sdl2.ext.FontManager.size` attribute, which gives a default size
  to be used for adding fonts or rendering text
* updated :mod:`sdl2` to include the latest changes of SDL2
* :meth:`sdl2.ext.RenderContext.copy()` accepts any 4-value sequence as source
  or destination rectangle now
* issue #11: throw an :exc:`ImportError` instead of a
  :exc:`RuntimeError`, if a third-party DLL could not be imported
  properly
* fixed a bug in the installation code, which caused :mod:`sdl2.examples` not
  to install the required resources

Thanks to Steven Johnson for his enhancements to the FontManager class.
Thanks to Marcel Rodrigues for the improvements to RenderContext.copy().

0.5.0
------------
Released on 2013-08-14.

* new :class:`sdl2.ext.FontManager` class, which provides simple TTF font
  rendering.
* new :meth:`sdl2.ext.SpriteFactory.from_text()` method, which creates
  text sprites
* put the SDL2 dll path at the beginning of PATH, if a PYSDL2_DLL_PATH
  is provided to avoid loading issues for third party DLLs on Win32
  platforms
* minor documentation fixes

Thanks to Dan Gillett for providing the FontManager and from_text()
enhancements and his patience regarding all the small change requests.
Thanks to Mihail Latyshov for providing fixes to the documentation.


0.4.1
------------
Released on 2013-07-26.

* updated :mod:`sdl2` to include the latest changes of SDL2
* improved DLL detection for DLLs not being in a library path
* fixed a bug in :meth:`sdl2.ext.RenderContext.draw_rect()` for drawing
  a single rect
* fixed a bug in the :func:`repr` call for :class:`sdl2.ext.SoftwareSprite`
* issue #4: fixed a bug in :meth:`sdl2.ext.RenderContext.fill()` for filling
  a single rect
* issue #5: fixed pip installation support
* issue #6: fixed a bug in :func:`sdl2.ext.get_events()`, which did not handle
  more than 10 events in the queue correctly
* issue #8: :meth:`sdl2.ext.SpriteFactory.create_texture_sprite` can
  create sprites to be used as rendering targets now
* issue #9: improved error messages on trying to bind non-existent library
  functions via ctypes
* minor documentation fixes

Thanks to Steven Johnson, Todd Rovito, Bil Bas and Dan McCombs for
providing fixes and improvements.

0.4.0
------------
Released on 2013-06-08.

* new :mod:`sdl2.sdlmixer` module, which provides access to the
  SDL2_mixer library
* issue #1: fixed libc loading for cases where libc.so is a ld script
* updated :mod:`sdl2` and :mod:`sdl2.sdlimage` to include the latest
  changes of the libraries, they wrap

0.3.0
------------
Released on 2013-05-07.

* new :mod:`sdl2.sdlgfx` module, which provides access to the SDL2_gfx library
* new :mod:`sdl2.ext.UIFactory.from_color` method; it creates UI-supportive
  sprites from a color
* fixed color argument bugs in :class:`sdl2.ext.RenderContext` methods
* fixed a module namespace issues in :mod:`sdl2.ext.pixelaccess`
* :mod:`sdl2.ext.SpriteFactory` methods do not use a default ``size`` argument
  anymore; it has to provided by the caller

0.2.0
------------
Released on 2013-05-03.

* removed sdl2.ext.scene; it now lives in python-utils
* fixed :mod:`sdl2.haptic` module usage for Python 3
* fixed :func:`sdl2.SDL_WindowGetData` and :func:`sdl2.SDL_WindowSetData`
  wrappers
* fixed :meth:`sdl2.ext.RenderContext.copy`
* fixed :mod:`sdl2.ext.font` module usage for Python 3
* fixed :func:`sdl2.ext.line`
* :mod:`sdl2` imports all submodules now
* improved documentation

0.1.0
------------
Released on 2013-04-23.

* Initial Release

.. |new| image:: new_icon.png


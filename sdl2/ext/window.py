"""Window routines to manage on-screen windows."""
from ctypes import c_int, byref
from .compat import byteify, stringify
from .common import SDLError
from .. import video

__all__ = ["Window", "get_display_mode"]


def get_display_mode(index=0):
    """Get information about the desktop display mode.

    Args:
        index (int): the index of the display to query. default to 0.
    Returns:
        tuple
    """
    dmode = video.SDL_DisplayMode()
    if video.SDL_GetDesktopDisplayMode(index, byref(dmode)):
        raise SDLError()
    return (dmode.w, dmode.h)


class Window(object):
    """A visible on-screen object with an optional border and title text.

    It represents an area on the screen that can be accessed by the
    application for displaying graphics and receive and process user
    input.
    """

    DEFAULTFLAGS = video.SDL_WINDOW_HIDDEN
    DEFAULTPOS = (video.SDL_WINDOWPOS_UNDEFINED,
                  video.SDL_WINDOWPOS_UNDEFINED)

    def __init__(self, title, size, position=None, flags=None):
        """Create a Window with a specific size and title.

        The position to show the Window at is undefined by default,
        letting the operating system or window manager pick the best
        location. The behaviour can be adjusted through the DEFAULTPOS
        class variable:

            Window.DEFAULTPOS = (10, 10)

        The created Window is hidden by default, which can be overridden
        at the time of creation by providing other SDL window flags
        through the flags parameter.

        The default flags for creating Window instances can be adjusted
        through the DEFAULTFLAGS class variable:

            Window.DEFAULTFLAGS = sdl2.video.SDL_WINDOW_SHOWN

        Attributes:
            window (sdl2.SDL_Window): The used SDL_Window.


        """
        if position is None:
            position = self.DEFAULTPOS
        if flags is None:
            flags = self.DEFAULTFLAGS
        window = video.SDL_CreateWindow(byteify(title, "utf-8"),
                                        position[0], position[1],
                                        size[0], size[1], flags)
        if not window:
            raise SDLError()
        self.window = window.contents

    def __del__(self):
        """Releases the resources of the Window, implicitly destroying the
        underlying SDL2 window."""
        if getattr(self, "window", None):
            video.SDL_DestroyWindow(self.window)
            self.window = None

    @property
    def title(self):
        """The title of the window."""
        return stringify(video.SDL_GetWindowTitle(self.window), "utf-8")

    @title.setter
    def title(self, value):
        """The title of the window."""
        video.SDL_SetWindowTitle(self.window, byteify(value, "utf-8"))

    @property
    def size(self):
        """The size of the window."""
        w, h = c_int(), c_int()
        video.SDL_GetWindowSize(self.window, byref(w), byref(h))
        return w.value, h.value

    def show(self):
        """Show the window on the display."""
        video.SDL_ShowWindow(self.window)

    def hide(self):
        """Hide the window."""
        video.SDL_HideWindow(self.window)

    def maximize(self):
        """Maximize the window to the display's dimensions."""
        video.SDL_MaximizeWindow(self.window)

    def minimize(self):
        """Minimize the window to an iconified state in the system tray."""
        video.SDL_MinimizeWindow(self.window)

    def refresh(self):
        """Refresh the entire window surface.

        This only needs to be called, if a SDL_Surface was acquired via
        get_surface() and is used to display contents.
        """
        video.SDL_UpdateWindowSurface(self.window)

    def get_surface(self):
        """Get the SDL_Surface used by the Window to display 2D pixel data.

        Using this method will make the usage of GL operations, such
        as texture handling, or using SDL renderers impossible.

        Returns:
            sdl2.SDL_Surface
        """
        sf = video.SDL_GetWindowSurface(self.window)
        if not sf:
            raise SDLError()
        return sf.contents

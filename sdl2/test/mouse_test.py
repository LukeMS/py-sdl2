
import sys
import unittest
try:
    from .. import mouse, events
    from ..ext import common
    from ..ext import events as ext_events
    from .. import ext as sdl2ext
    from .util.testutils import interactive, doprint
except SystemError:
    from sdl2 import mouse, events
    from sdl2.ext import common
    from sdl2.ext import events as ext_events
    from sdl2 import ext as sdl2ext
    from sdl2.test.util.testutils import interactive, doprint


class SDLMouseTest(unittest.TestCase):

    __tags__ = ["sdl"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    def test_PushMouseMotionEvent(self):
        ext_events.PushMouseMotionEvent(x=1, y=2)
        evs = common.get_events()
        self.assertEqual(len(evs), 1)
        ev = evs[0]

        self.assertEqual(ev.type, events.SDL_MOUSEMOTION)
        self.assertEqual(ev.motion.x, 1)
        self.assertEqual(ev.motion.y, 2)

    @unittest.skip("not implemented")
    def test_SDL_GetMouseFocus(self):
        pass

    def test_SDL_GetMouseState(self):
        mouse.SDL_GetMouseState(None, None)

    def test_SDL_GetRelativeMouseState(self):
        mouse.SDL_GetRelativeMouseState(None, None)

    @unittest.skipUnless(__name__ == '__main__', "interactive")
    @interactive("Was the cursor moved to the middle of the window?")
    def test_SDL_WarpMouseInWindow(self):
        window = sdl2ext.Window("Window", size=(64, 64))
        mouse.SDL_WarpMouseInWindow(window.window,
                                    32,
                                    32)
        window.show()
        doprint("A window should be shown with cursor centered on it.")

    @unittest.skip("not implemented")
    def test_SDL_GetSetRelativeMouseMode(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_CreateFreeCursor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_CreateColorCursor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_CreateSystemCursor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetSetCursor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetDefaultCursor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_ShowCursor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_WarpMouseGlobal(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_CaptureMouse(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetGlobalMouseState(self):
        pass

if __name__ == '__main__':
    sys.exit(unittest.main(verbosity=10))

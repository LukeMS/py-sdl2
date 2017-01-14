
import sys
import unittest

from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_EVERYTHING
from sdl2 import clipboard
from sdl2.stdinc import SDL_TRUE, SDL_FALSE

TEXT = 'i can has clipboardz?'
B_TEXT = TEXT.encode('utf-8')


class SDLClipboardTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def tearDown(self):
        SDL_Quit()

    def test_SDL_HasClipboardText(self):
        self.assertEqual(clipboard.SDL_SetClipboardText(None), 0)
        self.assertEqual(clipboard.SDL_HasClipboardText(), SDL_FALSE)

        self.assertEqual(clipboard.SDL_SetClipboardText(B_TEXT), 0)
        self.assertEqual(clipboard.SDL_HasClipboardText(), SDL_TRUE)

    def test_SDL_GetClipboardText(self):
        self.assertEqual(clipboard.SDL_SetClipboardText(B_TEXT), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, B_TEXT)

    def test_SDL_SetClipboardText(self):
        self.assertEqual(clipboard.SDL_SetClipboardText(b""), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"")

        self.assertEqual(clipboard.SDL_SetClipboardText(b"one"), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"one")

        self.assertEqual(clipboard.SDL_SetClipboardText(None), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"")


if __name__ == '__main__':
    sys.exit(unittest.main())

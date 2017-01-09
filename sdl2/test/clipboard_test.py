
import sys
import unittest
from tkinter import Tk
try:
    from .. import SDL_Init, SDL_Quit, SDL_INIT_EVERYTHING
    from .. import clipboard
    from ..stdinc import SDL_TRUE, SDL_FALSE
except SystemError:
    from sdl2 import (SDL_Init, SDL_Quit, SDL_INIT_EVERYTHING)
    from sdl2 import clipboard
    from sdl2.stdinc import SDL_TRUE, SDL_FALSE

TEXT = 'i can has clipboardz?'
B_TEXT = TEXT.encode('utf-8')


class SDLClipboardTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_EVERYTHING)
        self.tk = Tk()
        self.tk.withdraw()
        self.tk.clipboard_clear()
        self.tk.clipboard_append(TEXT)

    def tearDown(self):
        SDL_Quit()
        self.tk.clipboard_clear()
        self.tk.destroy()

    def test_SDL_HasClipboardText(self):
        self.assertEqual(clipboard.SDL_SetClipboardText(None), 0)
        self.assertEqual(clipboard.SDL_HasClipboardText(), SDL_FALSE)

        self.assertEqual(clipboard.SDL_SetClipboardText(B_TEXT), 0)
        self.assertEqual(clipboard.SDL_HasClipboardText(), SDL_TRUE)

    def test_SDL_GetClipboardText(self):
        self.tk.clipboard_clear()
        self.tk.clipboard_append(TEXT)

        retval = clipboard.SDL_GetClipboardText()

        self.assertEqual(retval, B_TEXT)

    def test_SDL_SetClipboardText(self):
        self.assertEqual(clipboard.SDL_SetClipboardText(B_TEXT), 0)
        retval = self.tk.selection_get(selection='CLIPBOARD')
        self.assertEqual(retval, TEXT)

        self.assertEqual(clipboard.SDL_SetClipboardText(b""), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"")

        self.assertEquals(clipboard.SDL_SetClipboardText(B_TEXT), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, B_TEXT)

        self.assertEquals(clipboard.SDL_SetClipboardText(None), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"")


if __name__ == '__main__':
    sys.exit(unittest.main())

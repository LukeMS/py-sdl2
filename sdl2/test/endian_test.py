
import sys
import math
import unittest
try:
    from .. import endian
except SystemError:
    from sdl2 import endian


class SDLEndianTest(unittest.TestCase):

    __tags__ = ["sdl"]

    def test_SDL_BYTEORDER(self):
        if sys.byteorder == "little":
            self.assertEqual(endian.SDL_BYTEORDER, endian.SDL_LIL_ENDIAN)
        else:
            self.assertEqual(endian.SDL_BYTEORDER, endian.SDL_BIG_ENDIAN)

    def test_SDL_Swap16(self):
        self.assertEqual(endian.SDL_Swap16(0xFF00), 0x00FF)
        self.assertEqual(endian.SDL_Swap16(0x0001), 0x0100)
        self.assertEqual(endian.SDL_Swap16(0x0032), 0x3200)
        self.assertEqual(endian.SDL_Swap16(0x0FF0), 0xF00F)
        self.assertEqual(endian.SDL_Swap16(0x00FF), 0xFF00)
        self.assertEqual(endian.SDL_Swap16(0x1234), 0x3412)
        if sys.byteorder == "little":
            self.assertEqual(endian.SDL_Swap16, endian.SDL_SwapBE16)
            self.assertNotEqual(endian.SDL_Swap16, endian.SDL_SwapLE16)
        else:
            self.assertNotEqual(endian.SDL_Swap16, endian.SDL_SwapBE16)
            self.assertEqual(endian.SDL_Swap16, endian.SDL_SwapLE16)

    def test_SDL_Swap32(self):
        self.assertEqual(endian.SDL_Swap32(0xFF000000), 0x000000FF)
        self.assertEqual(endian.SDL_Swap32(0x00FF0000), 0x0000FF00)
        self.assertEqual(endian.SDL_Swap32(0x0000FF00), 0x00FF0000)
        self.assertEqual(endian.SDL_Swap32(0x000000FF), 0xFF000000)
        self.assertEqual(endian.SDL_Swap32(0x12345678), 0x78563412)
        self.assertEqual(endian.SDL_Swap32(0xFF00FF00), 0x00FF00FF)
        if sys.byteorder == "little":
            self.assertEqual(endian.SDL_Swap32, endian.SDL_SwapBE32)
            self.assertNotEqual(endian.SDL_Swap32, endian.SDL_SwapLE32)
        else:
            self.assertNotEqual(endian.SDL_Swap32, endian.SDL_SwapBE32)
            self.assertEqual(endian.SDL_Swap32, endian.SDL_SwapLE32)

    def test_SDL_Swap64(self):
        self.assertEqual(endian.SDL_Swap64(0xFF00000000000000),
                         0x00000000000000FF)
        self.assertEqual(endian.SDL_Swap64(0x00FF000000000000),
                         0x000000000000FF00)
        self.assertEqual(endian.SDL_Swap64(0x0000FF0000000000),
                         0x0000000000FF0000)
        self.assertEqual(endian.SDL_Swap64(0x000000FF00000000),
                         0x00000000FF000000)
        self.assertEqual(endian.SDL_Swap64(0x00000000FF000000),
                         0x000000FF00000000)
        self.assertEqual(endian.SDL_Swap64(0x0000000000FF0000),
                         0x0000FF0000000000)
        self.assertEqual(endian.SDL_Swap64(0x000000000000FF00),
                         0x00FF000000000000)
        self.assertEqual(endian.SDL_Swap64(0x00000000000000FF),
                         0xFF00000000000000)
        self.assertEqual(endian.SDL_Swap64(0x0123456789ABCDEF),
                         0xEFCDAB8967452301)
        if sys.byteorder == "little":
            self.assertEqual(endian.SDL_Swap64, endian.SDL_SwapBE64)
            self.assertNotEqual(endian.SDL_Swap64, endian.SDL_SwapLE64)
        else:
            self.assertNotEqual(endian.SDL_Swap64, endian.SDL_SwapBE64)
            self.assertEqual(endian.SDL_Swap64, endian.SDL_SwapLE64)

    def test_SDL_SwapFloat(self):
        v = -100.0
        while v < 101:
            p = endian.SDL_SwapFloat(v)
            self.assertNotEqual(p, v)
            self.assertEqual(endian.SDL_SwapFloat(p), v)
            v += 0.1
        values = (sys.float_info.epsilon,
                  sys.float_info.min,
                  sys.float_info.max,
                  - sys.float_info.min,
                  math.pi,
                  - math.pi
                  )
        for v in values:
            p = endian.SDL_SwapFloat(v)
            self.assertNotEqual(p, v)
            self.assertEqual(endian.SDL_SwapFloat(p), v)

        if sys.byteorder == "little":
            self.assertEqual(endian.SDL_SwapFloat, endian.SDL_SwapFloatBE)
            self.assertNotEqual(endian.SDL_SwapFloat, endian.SDL_SwapFloatLE)
        else:
            self.assertNotEqual(endian.SDL_SwapFloat, endian.SDL_SwapFloatBE)
            self.assertEqual(endian.SDL_SwapFloat, endian.SDL_SwapFloatLE)


if __name__ == '__main__':
    sys.exit(unittest.main())

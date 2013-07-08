import sys
import ctypes
import unittest
from .. import version


class SDLVersionTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_version(self):
        v = version.SDL_version(0, 0, 0)
        self.assertEqual(v.major, 0)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)

    def test_SDL_GetVersion(self):
        v = version.SDL_version()
        version.SDL_GetVersion(ctypes.byref(v))
        self.assertEqual(type(v), version.SDL_version)
        self.assertEqual(v.major, 2)
        self.assertEqual(v.minor, 0)
        self.assertEqual(v.patch, 0)

    def test_SDL_VERSIONNUM(self):
        self.assertEqual(version.SDL_VERSIONNUM(1, 2, 3), 1203)
        self.assertEqual(version.SDL_VERSIONNUM(4, 5, 6), 4506)
        self.assertEqual(version.SDL_VERSIONNUM(2, 0, 0), 2000)
        self.assertEqual(version.SDL_VERSIONNUM(17, 42, 3), 21203)

    def test_SDL_VERSION_ATLEAST(self):
        self.assertTrue(version.SDL_VERSION_ATLEAST(1, 2, 3))
        self.assertTrue(version.SDL_VERSION_ATLEAST(2, 0, 0))
        self.assertFalse(version.SDL_VERSION_ATLEAST(2, 0, 1))

    def test_SDL_GetRevision(self):
        self.assertEqual(version.SDL_GetRevision()[0:3], b"hg-")

    def test_SDL_GetRevisionNumber(self):
        if sys.platform in ("win32", "cli"):
            # HG tip on Win32 does not set any revision number
            self.assertGreaterEqual(version.SDL_GetRevisionNumber(), 0)
        else:
            self.assertGreaterEqual(version.SDL_GetRevisionNumber(), 7000)


if __name__ == '__main__':
    sys.exit(unittest.main())


import sys
import unittest

from sdl2 import version
try:
    from sdl2 import sdlmixer
except ImportError:
    HAS_MIXER = False
else:
    HAS_MIXER = True


class SDLMixerTest(unittest.TestCase):

    __tags__ = ["sdl", "sdlmixer"]

    def setUp(self):
        sdlmixer.Mix_Init(0)

    def tearDown(self):
        sdlmixer.Mix_Quit()

    @unittest.skipUnless(HAS_MIXER, "requires sdlmixer")
    def test_Mix_Linked_Version(self):
        v = sdlmixer.Mix_Linked_Version()
        self.assertIsInstance(v.contents, version.SDL_version)
        self.assertEqual(v.contents.major, 2)
        self.assertEqual(v.contents.minor, 0)
        self.assertEqual(v.contents.patch, 1)

if __name__ == '__main__':
    sys.exit(unittest.main())

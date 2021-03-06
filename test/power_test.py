
from ctypes import c_int, byref
import os
import sys
import unittest

from sdl2 import power
from sdl2.util import get_cfg
from sdl2.util.test_utils import interactive, doprint

INTERACTIVE = get_cfg(
    path=os.path.join(
        os.path.dirname(__file__), 'sdl2_test.cfg'),
    convert=True,
    section="DEFAULT",
    option="INTERACTIVE")


class SDLPowerTest(unittest.TestCase):

    __tags__ = ["sdl"]

    def test_basic(self):
        secs, percent = c_int(), c_int()
        power.SDL_GetPowerInfo(byref(secs), byref(percent))

    @unittest.skipUnless(INTERACTIVE, "interactive")
    @interactive("Do the shown numbers match your power supply status?")
    def test_get_power_info(self):
        secs, percent = c_int(), c_int()
        retval = power.SDL_GetPowerInfo(byref(secs), byref(percent))
        state = "Unknown"
        if retval == power.SDL_POWERSTATE_ON_BATTERY:
            state = "On battery"
        elif retval == power.SDL_POWERSTATE_NO_BATTERY:
            state = "No battery"
        elif retval == power.SDL_POWERSTATE_CHARGING:
            state = "Battery charging"
        elif retval == power.SDL_POWERSTATE_CHARGED:
            state = "Battery charged"
        output = "Power Status: %s" % state + os.linesep
        output += "Minutes left (-1 = undetermined): %d" % (secs.value / 60)
        output += os.linesep
        output += "Percent left (-1 = undetermined): %d" % percent.value
        output += os.linesep
        doprint(output)


if __name__ == '__main__':
    sys.exit(unittest.main())

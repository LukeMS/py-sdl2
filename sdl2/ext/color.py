"""Color module for color creation and conversion operations."""
# support for Python 2.6, 2.7
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.standard_library import install_aliases
install_aliases()
import struct
from builtins import *
from future.utils import raise_from

from math import floor


__all__ = ["Color", "is_rgb_color", "is_rgba_color", "argb_to_color", "ARGB",
           "rgba_to_color", "RGBA", "string_to_color", "convert_to_color",
           "COLOR"]


class Color(object):
    """A simple RGBA-based color implementation."""

    __slots__ = ("_r", "_g", "_b", "_a")

    def __init__(self, r=255, g=255, b=255, a=255):
        """Create a Color with the specified RGBA values."""
        try:
            for c in (r, g, b, a):
                assert 0 <= c <= 255
        except AssertionError as e:
            raise_from(ValueError("r must be in the range [0; 255]"), e)
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)
        self._a = int(a)

    def __repr__(self):
        return ("Color(r=%d, g=%d, b=%d, a=%d)" %
                (self.r, self.g, self.b, self.a))

    def __copy__(self):
        return Color(self.r, self.g, self.b, self.a)

    def __eq__(self, color):
        return (self.r == color.r and self.g == color.g and
                self.b == color.b and self.a == color.a)

    def __ne__(self, color):
        return (self.r != color.r or self.g != color.g or
                self.b != color.b or self.a != color.a)

    def __int__(self):
        return (self.r << 24 | self.g << 16 | self.b << 8 | self.a)

    def __long__(self):
        return (self.r << 24 | self.g << 16 | self.b << 8 | self.a)

    def __float__(self):
        return (self.r << 24 | self.g << 16 | self.b << 8 | self.a) * 1.0

    def __index__(self):
        return (self.r << 24 | self.g << 16 | self.b << 8 | self.a)

    def __oct__(self):
        val = (self.r << 24 | self.g << 16 | self.b << 8 | self.a)
        return oct(val)

    def __hex__(self):
        val = (self.r << 24 | self.g << 16 | self.b << 8 | self.a)
        return hex(val)

    def __invert__(self):
        vals = (255 - self.r, 255 - self.g, 255 - self.b, 255 - self.a)
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __mod__(self, color):
        vals = (self.r % color.r, self.g % color.g, self.b % color.b,
                self.a % color.a)
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __div__(self, color):
        vals = [0, 0, 0, 0]
        if color.r != 0:
            vals[0] = self.r / color.r
        if color.g != 0:
            vals[1] = self.g / color.g
        if color.b != 0:
            vals[2] = self.b / color.b
        if color.a != 0:
            vals[3] = self.a / color.a
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __truediv__(self, color):
        vals = [0, 0, 0, 0]
        if color.r != 0:
            vals[0] = self.r / color.r
        if color.g != 0:
            vals[1] = self.g / color.g
        if color.b != 0:
            vals[2] = self.b / color.b
        if color.a != 0:
            vals[3] = self.a / color.a
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __mul__(self, color):
        vals = (min(self.r * color.r, 255), min(self.g * color.g, 255),
                min(self.b * color.b, 255), min(self.a * color.a, 255))
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __sub__(self, color):
        vals = (max(self.r - color.r, 0), max(self.g - color.g, 0),
                max(self.b - color.b, 0), max(self.a - color.a, 0))
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __add__(self, color):
        vals = (min(self.r + color.r, 255), min(self.g + color.g, 255),
                min(self.b + color.b, 255), min(self.a + color.a, 255))
        return Color(vals[0], vals[1], vals[2], vals[3])

    def __len__(self):
        return 4

    def __getitem__(self, index):
        return (self.r, self.g, self.b, self.a)[index]

    def __setitem__(self, index, val):
        tmp = [self.r, self.g, self.b, self.a]
        tmp[index] = val
        self.r = tmp[0]
        self.g = tmp[1]
        self.b = tmp[2]
        self.a = tmp[3]

    @property
    def r(self):
        """Gets or sets the red value of the Color."""
        return self._r

    @r.setter
    def r(self, val):
        """Gets or sets the red value of the Color."""
        if type(val) not in(int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._r = val

    @property
    def g(self):
        """Gets or sets the green value of the Color."""
        return self._g

    @g.setter
    def g(self, val):
        """Gets or sets the green value of the Color."""
        if type(val) not in(int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._g = val

    @property
    def b(self):
        """Gets or sets the blue value of the Color."""
        return self._b

    @b.setter
    def b(self, val):
        """Gets or sets the blue value of the Color."""
        if type(val) not in(int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._b = val

    @property
    def a(self):
        """Gets or sets the alpha value of the Color."""
        return self._a

    @a.setter
    def a(self, val):
        """Gets or sets the alpha value of the Color."""
        if type(val) not in(int, long):
            raise TypeError("value must be an int")
        if val < 0 or val > 255:
            raise ValueError("The value must be in the range [0; 255]")
        self._a = val

    @property
    def hsva(self):
        """The Color as HSVA value."""
        rn = self.r / 255.0
        gn = self.g / 255.0
        bn = self.b / 255.0
        an = self.a / 255.0

        maxv = max(rn, gn, bn)
        minv = min(rn, gn, bn)
        diff = maxv - minv

        h = 0
        s = 0
        v = maxv * 100.0
        a = an * 100.0

        if maxv == minv:
            return(h, s, v, a)
        s = 100.0 * (maxv - minv) / maxv

        if maxv == rn:
            h = (60 * (gn - bn) / diff) % 360.0
        elif maxv == gn:
            h = (60 * (bn - rn) / diff) + 120.0
        else:
            h = (60 * (rn - gn) / diff) + 240.0
        if h < 0:
            h += 360.0
        return (h, s, v, a)

    @hsva.setter
    def hsva(self, value):
        """The Color as HSVA value."""
        h, s, v, a = value
        for x in (h, s, v, a):
            if type(x) not in(int, long, float):
                raise TypeError("HSVA values must be of type float")
        if not (0 <= s <= 100) or not (0 <= v <= 100) or \
                not (0 <= a <= 100) or not (0 <= h <= 360):
            raise ValueError("invalid HSVA value")

        self.a = int((a / 100.0) * 255)
        s /= 100.0
        v /= 100.0

        hi = int(floor(h / 60.0))
        f = (h / 60.0) - hi
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        if hi == 0:
            self.r = int(v * 255)
            self.g = int(t * 255)
            self.b = int(p * 255)
        elif hi == 1:
            self.r = int(q * 255)
            self.g = int(v * 255)
            self.b = int(p * 255)
        elif hi == 2:
            self.r = int(p * 255)
            self.g = int(v * 255)
            self.b = int(t * 255)
        elif hi == 3:
            self.r = int(p * 255)
            self.g = int(q * 255)
            self.b = int(v * 255)
        elif hi == 4:
            self.r = int(t * 255)
            self.g = int(p * 255)
            self.b = int(v * 255)
        elif hi == 5:
            self.r = int(v * 255)
            self.g = int(p * 255)
            self.b = int(q * 255)
        else:
            raise OverflowError("invalid HSVA value")

    @property
    def hsla(self):
        """The Color a HSLA value."""
        rn = self.r / 255.0
        gn = self.g / 255.0
        bn = self.b / 255.0
        an = self.a / 255.0

        maxv = max(rn, gn, bn)
        minv = min(rn, gn, bn)
        diff = maxv - minv

        h = 0
        s = 0
        l = 50.0 * (maxv + minv)
        a = an * 100.0

        if maxv == minv:
            return(h, s, l, a)

        if l <= 50.0:
            s = diff / (maxv + minv) * 100.0
        else:
            s = diff / (2.0 - maxv - minv) * 100.0

        if maxv == rn:
            h = (60 * (gn - bn) / diff) % 360.0
        elif maxv == gn:
            h = (60 * (bn - rn) / diff) + 120.0
        else:
            h = (60 * (rn - gn) / diff) + 240.0
        if h < 0:
            h += 360.0
        return (h, s, l, a)

    @hsla.setter
    def hsla(self, value):
        """The Color a HSLA value."""
        h, s, l, a = value
        for x in (h, s, l, a):
            if type(x) not in (int, long, float):
                raise TypeError("HSLA values must be of type float")
        if not (0 <= s <= 100) or not (0 <= l <= 100) or \
                not (0 <= a <= 100) or not (0 <= h <= 360):
            raise ValueError("invalid HSLA value")

        self.a = int((a / 100.0) * 255)

        s /= 100.0
        l /= 100.0

        if s == 0:
            self.r = int(l * 255)
            self.g = int(l * 255)
            self.b = int(l * 255)
            return

        q = 0
        if l < 0.5:
            q = l * (1 + s)
        else:
            q = l + s - (l * s)
        p = 2 * l - q

        ht = h / 360.0

        # r
        h = ht + (1.0 / 3.0)
        if h < 0:
            h += 1
        elif h > 1:
            h -= 1

        if h < (1.0 / 6.0):
            self.r = int((p + ((q - p) * 6 * h)) * 255)
        elif h < 0.5:
            self.r = int(q * 255)
        elif h < (2.0 / 3.0):
            self.r = int((p + ((q - p) * 6 * (2.0 / 3.0 - h))) * 255)
        else:
            self.r = int(p * 255)

        # g
        h = ht
        if h < 0:
            h += 1
        elif h > 1:
            h -= 1

        if h < (1.0 / 6.0):
            self.g = int((p + ((q - p) * 6 * h)) * 255)
        elif h < 0.5:
            self.g = int(q * 255)
        elif h < (2.0 / 3.0):
            self.g = int((p + ((q - p) * 6 * (2.0 / 3.0 - h))) * 255)
        else:
            self.g = int(p * 255)

        # b
        h = ht - (1.0 / 3.0)
        if h < 0:
            h += 1
        elif h > 1:
            h -= 1

        if h < (1.0 / 6.0):
            self.b = int((p + ((q - p) * 6 * h)) * 255)
        elif h < 0.5:
            self.b = int(q * 255)
        elif h < (2.0 / 3.0):
            self.b = int((p + ((q - p) * 6 * (2.0 / 3.0 - h))) * 255)
        else:
            self.b = int(p * 255)

    @property
    def i1i2i3(self):
        """The Color as I1I2I3 value."""
        rn = self.r / 255.0
        gn = self.g / 255.0
        bn = self.b / 255.0

        i1 = (rn + gn + bn) / 3.0
        i2 = (rn - bn) / 2.0
        i3 = (2 * gn - rn - bn) / 4.0

        return(i1, i2, i3)

    @i1i2i3.setter
    def i1i2i3(self, value):
        """The Color as I1I2I3 value."""
        i1, i2, i3 = value
        for x in (i1, i2, i3):
            if type(x) not in (int, long, float):
                raise TypeError("I1I2I3 values must be of type float")
        if not (0 <= i1 <= 1) or not (-0.5 <= i2 <= 0.5) or \
                not (-0.5 <= i3 <= 0.5):
            raise ValueError("invalid I1I2I3 value")

        ab = i1 - i2 - 2 * i3 / 3.0
        ar = 2 * i2 + ab
        ag = 3 * i1 - ar - ab

        self.r = int(ar * 255)
        self.g = int(ag * 255)
        self.b = int(ab * 255)

    @property
    def cmy(self):
        """The Color as CMY value."""
        return (1.0 - self.r / 255.0,
                1.0 - self.g / 255.0,
                1.0 - self.b / 255.0)

    @cmy.setter
    def cmy(self, value):
        """The Color as CMY value."""
        c, m, y = value
        if (c < 0 or c > 1) or (m < 0 or m > 1) or (y < 0 or y > 1):
            raise ValueError("invalid CMY value")
        self.r = int((1.0 - c) * 255)
        self.g = int((1.0 - m) * 255)
        self.b = int((1.0 - y) * 255)

    def normalize(self):
        """Returns the RGBA values in a normalized form with the range
        [0;1] as tuple.
        """
        return (self.r / 255.0, self.g / 255.0, self.b / 255.0, self.a / 255.0)


def is_rgb_color(v):
    """Checks, if the passed value is an item that could be converted to
    a RGB color.
    """
    try:
        if hasattr(v, "r") and hasattr(v, "g") and hasattr(v, "b"):
            if 0 <= int(v.r) <= 255 and 0 <= int(v.g) <= 255 and \
                    0 <= v.b <= 255:
                return True

        if len(v) >= 3:
            if 0 <= int(v[0]) <= 255 and 0 <= int(v[1]) <= 255 and \
                    0 < int(v[2]) < 255:
                return True
        return False
    except (TypeError, ValueError):
        return False


def is_rgba_color(v):
    """Checks, if the passed value is an item that could be converted to
    a RGBA color.
    """
    rgb = is_rgb_color(v)
    if not rgb:
        return False

    try:
        if hasattr(v, "a") and 0 <= int(v.a) <= 255:
            return True
        if len(v) >= 4 and 0 <= int(v[3]) <= 255:
            return True
        return False
    except (TypeError, ValueError):
        return False


def argb_to_color(v):
    """Converts an integer value to a Color, assuming the integer
    represents a 32-bit ARGB value.
    """

    a = ((v & 0xFF000000) >> 24)
    r = ((v & 0x00FF0000) >> 16)
    g = ((v & 0x0000FF00) >> 8)
    b = ((v & 0x000000FF))
    return Color(r, g, b, a)


ARGB = argb_to_color


def rgba_to_color(v):
    """Converts an integer value to a Color, assuming the integer
    represents a 32-bit RGBBA value.
    """
    v = long(v)

    r = ((v & 0xFF000000) >> 24)
    g = ((v & 0x00FF0000) >> 16)
    b = ((v & 0x0000FF00) >> 8)
    a = ((v & 0x000000FF))
    return Color(r, g, b, a)


RGBA = rgba_to_color


def string_to_color(s):
    """Convert a hex color string or color name to a Color value.

    Supported hex values are:
    RGB
    RGBA
    RRGGBB
    RRGGBBAA
    #RGB
    #RGBA
    #RRGGBB
    #RRGGBBAA
    0xRGB
    0xRGBA
    0xRRGGBB
    0xRRGGBBAA
    """
    s = s.replace("0x", "", 1).replace("#", "", 1)

    s_len = len(s)
    if s_len == 3:
        s = "".join((s, "f"))
        s = "".join(c for ab in zip(s, s) for c in ab)
    elif s_len == 4:
        s = "".join(c for ab in zip(s, s) for c in ab)
    elif s_len == 6:
        s = "".join((s, "ff"))
    return Color(*struct.unpack('BBBB', bytes.fromhex(s)))


def convert_to_color(v):
    """Tries to convert the passed value to a Color object.

    If the color is an integer value, it is assumed to be in ARGB layout.
    """
    if isinstance(v, Color):
        return v
    if isinstance(v, str):
        return string_to_color(v)
    if isinstance(v, int):
        return argb_to_color(v)

    r, g, b, a = 0, 0, 0, 0
    if hasattr(v, "r") and hasattr(v, "g") and hasattr(v, "b"):
        if 0 <= int(v.r) <= 255 and 0 <= int(v.g) <= 255 and \
                0 <= v.b <= 255:
            r = int(v.r)
            g = int(v.g)
            b = int(v.b)
            if hasattr(v, "a") and 0 <= int(v.a) <= 255:
                a = int(v.a)
        else:
            raise ValueError("value is not Color-compatible")
        return Color(r, g, b, a)

    try:
        length = len(v)
    except:
        raise ValueError("value is not Color-compatible")
    if length < 3:
        raise ValueError("value is not Color-compatible")
    if (
        0 <= int(v[0]) <= 255 and
        0 <= int(v[1]) <= 255 and
        0 <= int(v[2]) <= 255
    ):
        r = int(v[0])
        g = int(v[1])
        b = int(v[2])
        if length >= 4 and 0 <= int(v[3]) <= 255:
            a = int(v[3])
        return Color(r, g, b, a)

    raise ValueError("value is not Color-compatible")


COLOR = convert_to_color

if __name__ == '__main__':

    """
    from timeit import Timer

    EMPTY_O = (
        "0x000",      "#000",
        "0x000f",     "#000f",
        "0x000000",   "#000000",
        "0x000000ff", "#000000ff"
    )
    EMPTY_A = (
        "0x0000",     "#0000",
        "0x00000000", "#00000000"
    )

    FULL_O = (
        "0xfff",      "#fff",
        "0xffff",     "#ffff",
        "0xffffff",   "#ffffff",
        "0xffffffff", "#ffffffff"
    )
    FULL_A = (
        "0xfff0",     "#fff0",
        "0xffffff00", "#ffffff00"
    )
    fn = {"string_to_color", "string_to_color_2"}
    results = {f: 0 for f in fn}
    for g in (EMPTY_O, EMPTY_A, FULL_O, FULL_A):
        for c in g:
            for f in fn:
                t = Timer(
                    setup=('from __main__ import %s' % f),
                    stmt="%s('%s')" % (f, c))
                results[f] += t.timeit(number=5000)
    print(results)
    """

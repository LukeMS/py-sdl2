
from __future__ import absolute_import, division, print_function
from builtins import *

import os
from setuptools import setup
import sys

VERSION = "0.10.0"

if __name__ == "__main__":
    if any(arg.startswith("bdist") for arg in sys.argv):
        if "--format=msi" in sys.argv or "bdist_msi" in sys.argv:
            # hack the version name to a format msi doesn't have trouble with
            VERSION = VERSION.replace("-alpha", "a")
            VERSION = VERSION.replace("-beta", "b")
            VERSION = VERSION.replace("-rc", "r")
    elif "test" in sys.argv:
        ext_modules = None

    fname = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "README.rst")
    readme = open(fname, "r")
    long_desc = readme.read().strip()
    long_desc = long_desc.split(":alt: Code Health")[-1]
    readme.close()

    setupdata = {
        "name": "PySDL2",
        "version": VERSION,
        "description": "Python SDL2 bindings",
        "long_description": long_desc,
        "author": "Marcus von Appen",
        "author_email": "marcus@sysfault.org",
        "license": "Public Domain / zlib",
        "url": "http://bitbucket.org/marcusva/py-sdl2",
        "download_url": "http://bitbucket.org/marcusva/py-sdl2/downloads",
        "package_dir": {"sdl2.examples": "examples"},
        "package_data": {"sdl2.examples": ["resources/*.*"]},
        "install_requires": [
            'pillow',
            'future',
        ],
        "packages": ["sdl2",
                     "sdl2.sdlgfx",
                     "sdl2.sdlimage",
                     "sdl2.sdlmixer",
                     "sdl2.sdlttf",
                     "sdl2.ext",
                     "sdl2.examples",
                     "sdl2.examples.ext",
                     "sdl2.examples.ext.rl"
                     ],
        "test_suite": "test",
        "classifiers": [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: Public Domain",
            "License :: OSI Approved :: zlib/libpng License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    }

    setup(**setupdata)

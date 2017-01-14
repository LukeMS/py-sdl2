.. _`rl_tutorial`:


Complete Roguelike Tutorial, using python 3 + pysdl2e 0.10
==========================================================


Welcome to the Complete Roguelike Tutorial!
-----------------------------------------


About this tutorial
*******************

The goal of this tutorial is to have a one-stop-shop for most of the info you need on how to build a Roguelike game from scratch. We hope you find it useful! We'll start with some quick Q&A. If you already know about Python, SDL2, pydl2, pysdl2e and/or is only interested in the implementation you can skip to `Complete Roguelike Tutorial - Part 1`_.


Inspiration
***********

This tutorial is heavily inspired by Jotaf's excellent `Complete roguelike tutorial using python + libtcod`_.

.. _`Complete roguelike tutorial using python + libtcod`: http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod


Why Python?
-----------
Most people familiar with this language will tell you it's fun! Python aims to be simple but powerful, and very accessible to beginners. This tutorial would probably be much harder without it. We insist that you install/use Python 3.x and go through at least the first parts of the `Python Tutorial`_. This tutorial will be much easier if you've experimented with the language first. Remember that the `Python Library Reference`_ is your friend -- the standard library has everything you might need and when programming you should be ready to search it for help on any unknown function you might encounter.

.. note:

   This tutorial is for Python 3 only, and it is strongly recommended that you use the Python 3.5 x86 release.

If you choose to use earlier versions of Python 3, you may encounter problems you need to overcome. File an issue_ about it and we'll work to fix tutorial or pysd2le.
If you choose to use Python 2, however, be aware this tutorial is not compatible with it, and there are no plans to support it.

.. _`Python Tutorial`: https://docs.python.org/tutorial
.. _`Python Library Reference`: https://docs.python.org/library/index.html
.. _issue`: https://github.com/LukeMS/py-sdl2/issues


Why SDL2?
---------

Simple DirectMedia Layer is a cross-platform development library designed to provide low level access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D. It is used by video playback software, emulators, and popular games including Valve_'s award winning catalog and many Humble Bundle games.
SDL officially supports Windows, Mac OS X, Linux, iOS, and Android. Support for other platforms may be found in the source code.
SDL is written in C, works natively with C++, and there are bindings available for several other languages, including C# and **Python**.
SDL 2.0 is distributed under the zlib license. This license allows you to use SDL *`freely in any software`_*.

SDL is extensively used in the industry in both large and small projects: `MobyGames listed 141 games using SDL`_ in 2017; the `SDL website itself listed around 700 games` in 2012; important commercial examples are `Angry Birds`_ or `Unreal Tournament`_; Open Source examples are OpenTTD_, `The Battle for Wesnoth`_ or Freeciv_; the PC game Homeworld_ was ported to the Pandora handheld and `Jagged Alliance 2`_ to Android via SDL; applications like the emulators DOSBox_, VisualBoyAdvance_ and ZSNES_ all use SDL; the `Source Engine`_ (on its Linux and Mac versions) and the CryEngine_ uses SDL.

A common misconception is that SDL is a game engine, but this is not true. However, the library is well-suited for building an engine on top of it. PySDL2 is a python wrapper for it, with much added functionalities. PySDL2e extends it, adding even functionalities that we will require to build our roguelike.

.. _Valve: https://valvesoftware.com/
.. _`Humble Bundle`: https://www.humblebundle.com
.. _`freely in any software`: https://www.libsdl.org/index.php
.. _`MobyGames listed 141 games using SDL`: https://www.mobygames.com/game-group/middleware-sdl/offset,0/so,4d/
.. _`SDL website itself listed around 700 games`: https://web.archive.org/web/20100629004347/https://www.libsdl.org/games.php?order=name&category=-1&completed=0&os=-1&match_name=&perpage=-1
.. _`Angry Birds`: https://en.wikipedia.org/wiki/Angry_Birds
.. _`Unreal Tournament]`: https://en.wikipedia.org/wiki/Unreal_Tournament
.. _OpenTTD: https://en.wikipedia.org/wiki/OpenTTD
.. _`The Battle for Wesnoth`: https://en.wikipedia.org/wiki/The_Battle_for_Wesnoth
.. _Freeciv: https://en.wikipedia.org/wiki/Freeciv
.. _Homeworld: https://en.wikipedia.org/wiki/Homeworld
.. _`Jagged Alliance 2`: https://en.wikipedia.org/wiki/Jagged_Alliance_2
.. _DOSBox]: https://en.wikipedia.org/wiki/DOSBox
.. _VisualBoyAdvance: https://en.wikipedia.org/wiki/VisualBoyAdvance
.. _ZSNES: https://en.wikipedia.org/wiki/ZSNES
.. _`Source Engine`: https://en.wikipedia.org/wiki/Source_(game_engine)
.. _CryEngine: https://en.wikipedia.org/wiki/CryEngine


What are PySDL2 and PySDL2e?
----------------------------
**PySDL2** is a wrapper around the SDL2 library. It has no licensing restrictions, nor does it rely on C code, but uses ctypes instead (considering that ctypes is part of Python's standard library, all you need is a python installation and `SDL2 runtime binaries`_.

.. note::

   In this tutorial we're using SDL2 version 2.0.5.

Other versions could work, but this tutorial do not guarantee compatibility with other versions - you're on your own for it.

**PySDL2e** is built on top of PySDL2, providing some extra functionalities that will make our journey through this tutorial a smooth one.

.. _`SDL2 runtime binaries`: https://www.libsdl.org/download-2.0.php


----


Complete Roguelike Tutorial - Part 0
====================================


Python
------

If you haven't already done so, `download and install Python 3.5`_. Any version of Python 3.x up to 3.5.x should be fine, but its not guaranteed to work.

PySDL2e is currently not working with Python 3.6.

.. note:

    This tutorial was written and tested using Windows 7 x64, Python 3.5.2 x86, PySDL2e 0.10 and SDL2 x86 2.0.5.

It is advisable to go with those versions for compatibility's sake.

.. _`download and install Python 3.5`: https://www.python.org/downloads/release/python-352/


PySDL2
------

The easiest way to install PySDL2 is using pip:


.. code-block:: bash

   python -m pip install https://github.com/LukeMS/py-sdl2/archive/master.zip

If you would like another form of installation you can look for it at `PySDL2e instrunctions`_,

.. _`PySDL2e instrunctions`: http://pysdl2.readthedocs.io/en/rel_0_9_5/install.html


SDL2
----

Download the `latest release of SDL2`_ and extract it somewhere. Be warned that both Python and SDL2 must either be **both 32 bit**, or **both 64 bit**.  If you get dll loading errors, getting this wrong is the most likely cause.
See `this page on PySDL2 documentation and choose a way to make you library visible` for PySDL2e.

.. _`this page on PySDL2 documentation and choose a way to make you library visible`: https://lukems.github.io/py-sdl2/integration.html#importing
.. _`latest release of SDL2`: https://www.libsdl.org/download-2.0.php


Choice of code editor
---------------------

If you're just starting out with Python, you'll find that many Python coders just use a simple editor and run their scripts from a console to see any debugging output. Most Python coders don't feel the need to use a fancy IDE! On Windows, Notepad++ is an excellent bet; most Linux programmers already have an editor of choice. Almost all editors allow you to configure shortcut keys (like F5 for instance) to quickly run the script you're editing, without having to switch to a console.


----


Complete Roguelike Tutorial - Part 1
====================================

Setting up your project
-----------------------

Create your project's folder. Inside it, create an empty files named ''rl.py''. It'll make the tutorial easier to just use the same names for now, and you can always rename it later.

.. code-block:: none

   +-roguelike-tutorial/
     |
     +-rl.py

If you chose to keep the SDL2 library at the project folder, it should now look like this:

.. code-block:: none

   +-roguelike-tutorial/
     |
     +-rl.py
     |
     +-SDL2-2.0.5.dll or libSDL2-2.0.5.so


Making sure everything is running
---------------------------------

Let's test PySDL2e's scene manager and an empty scene. This is just an example, when we implement our own scene we'kk go into more details.

.. literalinclude:: /../examples/ext/manager_scenebase.py
   :language: python


If it runs and looks green, we're ready to start!


Showing the @ on screen
------------------------

Our game is going to be based on PySDL2e's scene manager.
A scene manager keeps track of the scenes in a game, allowing us to switch between them. It provides a centralized place to load and unload the scenes, keeping track of which one is active and handling the unloading of inactive scenes.
Some possible scenes for a simple game would be: a title scene (or main menu scene); an options scene; a game scene; etc.
First we import the the :mod:`sdl2.ext.manager` module. It contains the :code:`Manager` and a basic scene (:code:`SceneBase`) which we will subclass. Our new scene class will be named :code:`SceneRogueLike`. At its initialization we'll create the sprite (stored as the attribute :class:`at`) and move it a little.

.. literalinclude:: /../examples/ext/rl/rl_part1_n.py
   :language: python
   :lines: 1-15


To create the sprite we used an instance of :class:`sdl2.ext.sprite.SpriteFactory` that both the :code:`Manager` and :code:`class SceneBase` carries at the attribute :code:`factory`, for our convenience.
Nothing will be show on the screen, however, until we create our :code:`on_update` function on the scene. It is the function intended to contain the graphical logic we write. One line of code inside the function should do the trick:

.. literalinclude:: /../examples/ext/rl/rl_part1_n.py
   :language: python
   :pyobject: SceneRogueLike.on_update

To render the sprite we've used an instance of :class:`sdl2.ext.sprite.SpriteRenderSystem` that the :code:`Manager` creates at its initialization. As we've seen with the :code:`factory`, both the :code:`Manager` and the :code:`SceneBase` keep it as an attribute.

After instantiating :class:Manager, we pass it our new :class:SceneRoguelike and tell it to run:

.. literalinclude:: /../examples/ext/rl/rl_part1_n.py
   :language: python
   :lines: 37-41

Ta-da! You're done. Run that code and see our `"@"` at the screen. It doesn't move yet, but we're getting there.
The source of what we've done so far can be found `here <https://github.com/LukeMS/py-sdl2/tree/master/examples/ext/rl/part1/rl_0.py>`_.


Moving around
-------------

That was pretty neat, huh? Now we're going to move around that @ with the keys!
We'll create the :code:`SceneRogueLike.on_key_release` function. At each loop the :code:`Manager` dispatches events to the active scene, and we're going to catch some of those:

.. literalinclude:: /../examples/ext/rl/rl_part1_n.py
   :language: python
   :pyobject: SceneRogueLike.on_key_release

Done! We having a responsive @.


----


Complete Roguelike Tutorial - Part 2
====================================

.. code-block:: none

   Off-screen consoles
   -------------------

   There's one small thing we need to get out of the way before we can continue. Notice that the drawing functions we called (console_set_default_foreground and console_put_char) have their first argument set to 0, meaning that they draw on the root console. This is the buffer that is shown directly on screen.
   It can be useful, however, to have other buffers to store the results of drawing functions without automatically showing them to the player. This is akin to drawing surfaces or buffers in other graphics libraries; but instead of pixels they store characters and colors so you can modify them at will. Some uses of these off-screen consoles include semi-transparency or fading effects and composing GUI panels by blitting them to different portions of the root console. We're going to draw on an off-screen console from now on. The main reason is that not doing so would mean that later on you can't compose different GUI panels as easily, or add certain effects.
   First, create a new off-screen console, which for now will occupy the whole screen, but this can be changed later. We'll use a simple name like con because it will be used a lot! You can put this in the initialization, right after console_init_root.

   >>>   con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

   Now change the first argument of console_put_char (there are 2 calls to this function) and console_set_default_foreground, from 0 to con. They're now drawing on the new console.
   Finally, just before console_flush(), blit the contents of the new console to the root console, to display them. The parameters may look a bit mysterious at first, but they're just saying that the source rectangle has its top-left corner at coordinates (0, 0) and is the same size as the screen; the destination coordinates are (0, 0) as well. Check the documentation on the console_blit function for more details.

   >>> libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

   That was a lot of talk for so little code and no visible change! The next section will surely be much more interesting, as we'll introduce our first dummy NPC among other things. Remember to check back the above documentation page when you get to coding your GUI.


Generalizing
------------

Now that we have the @ walking around, it would be a good idea to step back and think a bit about the design. Dealing directly with the :class:`sdl2.ext.sprite.Sprite` as our player worked so far, but it can quickly get out of control when you're defining things such as HP, bonuses, and inventory. We're going to take the opportunity to generalize a bit.
Now, there can be such a thing as over-generalization, but we'll try not to fall in that trap. What we're going to do is define the player as a :code:`GameObject`, by creating that class. It will act as a container for components and a interface to the sprite (now a component itself).
The neat thing is that the player will just be one instance of the :code:`GameObject` class -- it's general enough that you can re-use it to define items on the floor, monsters, doors, stairs; anything representable by a character on the screen. Here's the class, with the initialization, and two common methods :code:`move`, and :code:`render`. The code for rendering looks like the one we used on :code:`SceneRogueLike`, with a few changes.

.. literalinclude:: /../examples/ext/rl/rl_part2_n.py
   :language: python
   :pyobject: GameObject

Now we create the player as :code:`GameObject` instead of a Sprite. We'll also add it to a list that will hold all objects that are in the game. While we're at it we'll add a yellow '@' that represents a non-playing character, like in an RPG, just to test it out!
Here is our updated :code:`SceneRogueLike.__init__` function:

.. literalinclude:: /../examples/ext/rl/rl_part2_n.py
   :language: python
   :pyobject: SceneRogueLike.__init__

And here is our modified :code:`SceneRogueLike.on_update` function:

.. literalinclude:: /../examples/ext/rl/rl_part2_n.py
   :language: python
   :pyobject: SceneRogueLike.on_update

You can see the whole source code of our game below, if you want, or jump to `Complete Roguelike Tutorial - Part 3`_.


Source code up to this part
----------------------------

.. literalinclude:: /../examples/ext/rl/rl_part2_n.py
   :language: python


----


Complete Roguelike Tutorial - Part 3
====================================


The Map
-------

Just like how you generalized the concept of the player object, you'll now do the same thing with the dungeon map. After testing a few types I've concluded that nested lists provide good performance for the operations we're going to need to do over the map. So, internally, our :code:`Map` will store things as nested lists, but we're going to create a small interface to act over it.
We'll use a
We'll start by defining its size at the top of the file. We'll try to make this as configurable as possible, this should suffice for now!

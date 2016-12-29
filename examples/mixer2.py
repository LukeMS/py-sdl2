"""PySDL2 example: SDL_Mixer2 library.

Simple example that demonstrates how to use the SDL_Mixer2 library with
PySDL2.  This example was converted from the SDL Mixer tutorial here:
    http://www.kekkai.org/roger/sdl/mixer/

Removed the global variables and made the escape key quit the application.
Don't try and play sound without SDL_Mixer it is difficult.
"""

import os
import sys


from sdl2 import *
from sdl2.sdlmixer import *



def handleKey(key, phaser, phaserChannel):
    '''
    Press the 'p' key to hear the phaser or press escape to quit.
    '''
    if key.keysym.sym == SDLK_p:
        if key.type == SDL_KEYDOWN:
            if phaserChannel.value < 0:
                # Mix_PlayChannel takes, as its arguments, the channel that
                # the given sound should be played on, the sound itself, and
                # the number of times it should be looped.  If you don't
                # care what channel the sound plays on, just pass in -1.
                # Looping works like Mix_PlayMusic.  This function returns
                # the channel that the sound was assigned to, which you'll
                # need later.
                phaserChannel = Mix_PlayChannel(-1, phaser, -1)
        else:
            # Mix_HaltChannel stops a certain channel from playing - this
            # is one of the reasons we kept track of which channel the
            # phaser has been assigned to
            Mix_HaltChannel(phaserChannel)
            phaserChannel = -1
    if key.keysym.sym == SDLK_ESCAPE:
        if key.type == SDL_KEYDOWN:
            return False

    return True


def run():
    # every sound that gets played is assigned to a channel. Note that
    # this is different from the number of channels you request when you
    # open the audio device;  a channel in SDL_mixer holds information
    # about a sound sample that is playing, while the number of channels
    # you request when opening the device is dependent on what sort of
    # sound you want (1 channel = mono, 2 = stereo, etc)
    phaserChannel = c_int(-1)
    audio_rate = c_int(MIX_DEFAULT_FREQUENCY)
    audio_format = Uint16(MIX_DEFAULT_FORMAT)
    audio_channels = c_int(MIX_DEFAULT_CHANNELS)
    audio_buffers = c_int(4096)
    running = True
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)
    if Mix_OpenAudio(audio_rate, audio_format, audio_channels, audio_buffers):
        print("Unable to open audio!")
        return 1
    phaserFileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "resources", "phaser.wav")
    # we're going to pre-load the sound effects that we need right here
    phaser = Mix_LoadWAV(phaserFileName.encode("utf-8"))
    window = SDL_CreateWindow(b"mixer2.py", SDL_WINDOWPOS_CENTERED,
                              SDL_WINDOWPOS_CENTERED,
                              320, 240, SDL_WINDOW_SHOWN)
    while running:
        event = SDL_Event()
        while(SDL_PollEvent(event)):
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == SDL_KEYDOWN:
                running = handleKey(event.key, phaser, phaserChannel)
                break
            if event.type == SDL_KEYUP:
                running = handleKey(event.key, phaser, phaserChannel)
                break
        SDL_Delay(50)

    Mix_CloseAudio()
    SDL_DestroyWindow(window)
    SDL_Quit()

if __name__ == "__main__":
    sys.exit(run())

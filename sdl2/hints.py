from ctypes import c_int, c_char_p
from .dll import _bind
from .stdinc import SDL_bool

SDL_HINT_FRAMEBUFFER_ACCELERATION = b"SDL_FRAMEBUFFER_ACCELERATION"
SDL_HINT_RENDER_DRIVER = b"SDL_RENDER_DRIVER"
SDL_HINT_RENDER_OPENGL_SHADERS = b"SDL_RENDER_OPENGL_SHADERS"
SDL_HINT_RENDER_SCALE_QUALITY = b"SDL_RENDER_SCALE_QUALITY"
SDL_HINT_RENDER_VSYNC = b"SDL_RENDER_VSYNC"
SDL_HINT_VIDEO_X11_XVIDMODE = b"SDL_VIDEO_X11_XVIDMODE"
SDL_HINT_VIDEO_X11_XINERAMA = b"SDL_VIDEO_X11_XINERAMA"
SDL_HINT_VIDEO_X11_XRANDR = b"SDL_VIDEO_X11_XRANDR"
SDL_HINT_GRAB_KEYBOARD = b"SDL_GRAB_KEYBOARD"
SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS = b"SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"
SDL_HINT_IDLE_TIMER_DISABLED = b"SDL_IOS_IDLE_TIMER_DISABLED"
SDL_HINT_ORIENTATIONS = b"SDL_IOS_ORIENTATIONS"
SD_HINT_XINPUT_ENABLED = b"SDL_XINPUT_ENABLED"
SDL_HINT_GAMECONTROLLERCONFIG = b"SDL_GAMECONTROLLERCONFIG"
SDL_HINT_ALLOW_TOPMOST = b"SDL_ALLOW_TOPMOST"
SDL_HINT_DEFAULT = 0
SDL_HINT_NORMAL = 1
SDL_HINT_OVERRIDE = 2
SDL_HintPriority = c_int
SDL_SetHintWithPriority = _bind("SDL_SetHintWithPriority", [c_char_p, c_char_p, SDL_HintPriority], SDL_bool)
SDL_SetHint = _bind("SDL_SetHint", [c_char_p, c_char_p], SDL_bool)
SDL_GetHint = _bind("SDL_GetHint", [c_char_p], c_char_p)
SDL_ClearHints = _bind("SDL_ClearHints")

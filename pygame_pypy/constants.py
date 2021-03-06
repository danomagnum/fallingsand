""" pygame constants """

from pygame._sdl import sdl

# Event types
NOEVENT = sdl.SDL_NOEVENT
ACTIVEEVENT = sdl.SDL_ACTIVEEVENT
KEYDOWN = sdl.SDL_KEYDOWN
KEYUP = sdl.SDL_KEYUP
MOUSEMOTION = sdl.SDL_MOUSEMOTION
MOUSEBUTTONDOWN = sdl.SDL_MOUSEBUTTONDOWN
MOUSEBUTTONUP = sdl.SDL_MOUSEBUTTONUP
JOYAXISMOTION = sdl.SDL_JOYAXISMOTION
JOYBALLMOTION = sdl.SDL_JOYBALLMOTION
JOYHATMOTION = sdl.SDL_JOYHATMOTION
JOYBUTTONDOWN = sdl.SDL_JOYBUTTONDOWN
JOYBUTTONUP = sdl.SDL_JOYBUTTONUP
QUIT = sdl.SDL_QUIT
SYSWMEVENT = sdl.SDL_SYSWMEVENT
EVENT_RESERVEDA = sdl.SDL_EVENT_RESERVEDA
EVENT_RESERVEDB = sdl.SDL_EVENT_RESERVEDB
VIDEORESIZE = sdl.SDL_VIDEORESIZE
VIDEOEXPOSE = sdl.SDL_VIDEOEXPOSE
EVENT_RESERVED2 = sdl.SDL_EVENT_RESERVED2
EVENT_RESERVED3 = sdl.SDL_EVENT_RESERVED3
EVENT_RESERVED4 = sdl.SDL_EVENT_RESERVED4
EVENT_RESERVED5 = sdl.SDL_EVENT_RESERVED5
EVENT_RESERVED6 = sdl.SDL_EVENT_RESERVED6
EVENT_RESERVED7 = sdl.SDL_EVENT_RESERVED7
USEREVENT = sdl.SDL_USEREVENT
NUMEVENTS = sdl.SDL_NUMEVENTS
USEREVENT_DROPFILE = 0x1000

# Surface things
SWSURFACE = sdl.SDL_SWSURFACE
HWSURFACE = sdl.SDL_HWSURFACE

LIL_ENDIAN = sdl.SDL_LIL_ENDIAN

FULLSCREEN = sdl.SDL_FULLSCREEN
RESIZABLE = sdl.SDL_RESIZABLE
NOFRAME = sdl.SDL_NOFRAME

DOUBLEBUF = sdl.SDL_DOUBLEBUF

HWACCEL = sdl.SDL_HWACCEL

ASYNCBLIT = sdl.SDL_ASYNCBLIT

RLEACCEL = sdl.SDL_RLEACCEL
RLEACCELOK = sdl.SDL_RLEACCELOK

SRCALPHA = sdl.SDL_SRCALPHA
SRCCOLORKEY = sdl.SDL_SRCCOLORKEY
HWPALETTE = sdl.SDL_HWPALETTE

ANYFORMAT = sdl.SDL_ANYFORMAT

BLEND_RGB_ADD = 0x01
BLEND_RGB_SUB = 0x02
BLEND_RGB_MULT = 0x03
BLEND_RGB_MIN = 0x04
BLEND_RGB_MAX = 0x05
BLEND_RGBA_ADD = 0x06
BLEND_RGBA_SUB = 0x07
BLEND_RGBA_MULT = 0x08
BLEND_RGBA_MIN = 0x09
BLEND_RGBA_MAX = 0x10
BLEND_PREMULTIPLIED = 0x11

BLEND_ADD = BLEND_RGB_ADD
BLEND_SUB = BLEND_RGB_SUB
BLEND_MULT = BLEND_RGB_MULT
BLEND_MIN = BLEND_RGB_MIN
BLEND_MAX = BLEND_RGB_MAX

# OpenGL stuff
OPENGL = sdl.SDL_OPENGL
GL_RED_SIZE = sdl.SDL_GL_RED_SIZE
GL_GREEN_SIZE = sdl.SDL_GL_GREEN_SIZE
GL_BLUE_SIZE = sdl.SDL_GL_BLUE_SIZE
GL_ALPHA_SIZE = sdl.SDL_GL_ALPHA_SIZE
GL_BUFFER_SIZE = sdl.SDL_GL_BUFFER_SIZE
GL_DOUBLEBUFFER = sdl.SDL_GL_DOUBLEBUFFER
GL_DEPTH_SIZE = sdl.SDL_GL_DEPTH_SIZE
GL_STENCIL_SIZE = sdl.SDL_GL_STENCIL_SIZE
GL_ACCUM_RED_SIZE = sdl.SDL_GL_ACCUM_RED_SIZE
GL_ACCUM_GREEN_SIZE = sdl.SDL_GL_ACCUM_GREEN_SIZE
GL_ACCUM_BLUE_SIZE = sdl.SDL_GL_ACCUM_BLUE_SIZE
GL_ACCUM_ALPHA_SIZE = sdl.SDL_GL_ACCUM_ALPHA_SIZE
GL_STEREO = sdl.SDL_GL_STEREO
GL_MULTISAMPLEBUFFERS = sdl.SDL_GL_MULTISAMPLEBUFFERS
GL_MULTISAMPLESAMPLES = sdl.SDL_GL_MULTISAMPLESAMPLES
GL_ACCELERATED_VISUAL = sdl.SDL_GL_ACCELERATED_VISUAL
GL_SWAP_CONTROL = sdl.SDL_GL_SWAP_CONTROL

# Keys
from pygame._sdl_keys import *

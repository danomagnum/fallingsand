"""Special separate FFI module for keyboard constants.

These are enums that take many long seconds to build and they don't change at
all, so having them in a separate FFI unit makes startup faster when we've
changed the cdef and have to rebuild.
"""

import cffi

ffi = cffi.FFI()

ffi.cdef("""
typedef enum {
    SDLK_UNKNOWN,
    SDLK_FIRST,
    SDLK_BACKSPACE,
    SDLK_TAB,
    SDLK_CLEAR,
    SDLK_RETURN,
    SDLK_PAUSE,
    SDLK_ESCAPE,
    SDLK_SPACE,
    SDLK_EXCLAIM,
    SDLK_QUOTEDBL,
    SDLK_HASH,
    SDLK_DOLLAR,
    SDLK_AMPERSAND,
    SDLK_QUOTE,
    SDLK_LEFTPAREN,
    SDLK_RIGHTPAREN,
    SDLK_ASTERISK,
    SDLK_PLUS,
    SDLK_COMMA,
    SDLK_MINUS,
    SDLK_PERIOD,
    SDLK_SLASH,
    SDLK_0,
    SDLK_1,
    SDLK_2,
    SDLK_3,
    SDLK_4,
    SDLK_5,
    SDLK_6,
    SDLK_7,
    SDLK_8,
    SDLK_9,
    SDLK_COLON,
    SDLK_SEMICOLON,
    SDLK_LESS,
    SDLK_EQUALS,
    SDLK_GREATER,
    SDLK_QUESTION,
    SDLK_AT,
    SDLK_LEFTBRACKET,
    SDLK_BACKSLASH,
    SDLK_RIGHTBRACKET,
    SDLK_CARET,
    SDLK_UNDERSCORE,
    SDLK_BACKQUOTE,
    SDLK_a,
    SDLK_b,
    SDLK_c,
    SDLK_d,
    SDLK_e,
    SDLK_f,
    SDLK_g,
    SDLK_h,
    SDLK_i,
    SDLK_j,
    SDLK_k,
    SDLK_l,
    SDLK_m,
    SDLK_n,
    SDLK_o,
    SDLK_p,
    SDLK_q,
    SDLK_r,
    SDLK_s,
    SDLK_t,
    SDLK_u,
    SDLK_v,
    SDLK_w,
    SDLK_x,
    SDLK_y,
    SDLK_z,
    SDLK_DELETE,
    SDLK_WORLD_0,
    SDLK_WORLD_1,
    SDLK_WORLD_2,
    SDLK_WORLD_3,
    SDLK_WORLD_4,
    SDLK_WORLD_5,
    SDLK_WORLD_6,
    SDLK_WORLD_7,
    SDLK_WORLD_8,
    SDLK_WORLD_9,
    SDLK_WORLD_10,
    SDLK_WORLD_11,
    SDLK_WORLD_12,
    SDLK_WORLD_13,
    SDLK_WORLD_14,
    SDLK_WORLD_15,
    SDLK_WORLD_16,
    SDLK_WORLD_17,
    SDLK_WORLD_18,
    SDLK_WORLD_19,
    SDLK_WORLD_20,
    SDLK_WORLD_21,
    SDLK_WORLD_22,
    SDLK_WORLD_23,
    SDLK_WORLD_24,
    SDLK_WORLD_25,
    SDLK_WORLD_26,
    SDLK_WORLD_27,
    SDLK_WORLD_28,
    SDLK_WORLD_29,
    SDLK_WORLD_30,
    SDLK_WORLD_31,
    SDLK_WORLD_32,
    SDLK_WORLD_33,
    SDLK_WORLD_34,
    SDLK_WORLD_35,
    SDLK_WORLD_36,
    SDLK_WORLD_37,
    SDLK_WORLD_38,
    SDLK_WORLD_39,
    SDLK_WORLD_40,
    SDLK_WORLD_41,
    SDLK_WORLD_42,
    SDLK_WORLD_43,
    SDLK_WORLD_44,
    SDLK_WORLD_45,
    SDLK_WORLD_46,
    SDLK_WORLD_47,
    SDLK_WORLD_48,
    SDLK_WORLD_49,
    SDLK_WORLD_50,
    SDLK_WORLD_51,
    SDLK_WORLD_52,
    SDLK_WORLD_53,
    SDLK_WORLD_54,
    SDLK_WORLD_55,
    SDLK_WORLD_56,
    SDLK_WORLD_57,
    SDLK_WORLD_58,
    SDLK_WORLD_59,
    SDLK_WORLD_60,
    SDLK_WORLD_61,
    SDLK_WORLD_62,
    SDLK_WORLD_63,
    SDLK_WORLD_64,
    SDLK_WORLD_65,
    SDLK_WORLD_66,
    SDLK_WORLD_67,
    SDLK_WORLD_68,
    SDLK_WORLD_69,
    SDLK_WORLD_70,
    SDLK_WORLD_71,
    SDLK_WORLD_72,
    SDLK_WORLD_73,
    SDLK_WORLD_74,
    SDLK_WORLD_75,
    SDLK_WORLD_76,
    SDLK_WORLD_77,
    SDLK_WORLD_78,
    SDLK_WORLD_79,
    SDLK_WORLD_80,
    SDLK_WORLD_81,
    SDLK_WORLD_82,
    SDLK_WORLD_83,
    SDLK_WORLD_84,
    SDLK_WORLD_85,
    SDLK_WORLD_86,
    SDLK_WORLD_87,
    SDLK_WORLD_88,
    SDLK_WORLD_89,
    SDLK_WORLD_90,
    SDLK_WORLD_91,
    SDLK_WORLD_92,
    SDLK_WORLD_93,
    SDLK_WORLD_94,
    SDLK_WORLD_95,
    SDLK_KP0,
    SDLK_KP1,
    SDLK_KP2,
    SDLK_KP3,
    SDLK_KP4,
    SDLK_KP5,
    SDLK_KP6,
    SDLK_KP7,
    SDLK_KP8,
    SDLK_KP9,
    SDLK_KP_PERIOD,
    SDLK_KP_DIVIDE,
    SDLK_KP_MULTIPLY,
    SDLK_KP_MINUS,
    SDLK_KP_PLUS,
    SDLK_KP_ENTER,
    SDLK_KP_EQUALS,
    SDLK_UP,
    SDLK_DOWN,
    SDLK_RIGHT,
    SDLK_LEFT,
    SDLK_INSERT,
    SDLK_HOME,
    SDLK_END,
    SDLK_PAGEUP,
    SDLK_PAGEDOWN,
    SDLK_F1,
    SDLK_F2,
    SDLK_F3,
    SDLK_F4,
    SDLK_F5,
    SDLK_F6,
    SDLK_F7,
    SDLK_F8,
    SDLK_F9,
    SDLK_F10,
    SDLK_F11,
    SDLK_F12,
    SDLK_F13,
    SDLK_F14,
    SDLK_F15,
    SDLK_NUMLOCK,
    SDLK_CAPSLOCK,
    SDLK_SCROLLOCK,
    SDLK_RSHIFT,
    SDLK_LSHIFT,
    SDLK_RCTRL,
    SDLK_LCTRL,
    SDLK_RALT,
    SDLK_LALT,
    SDLK_RMETA,
    SDLK_LMETA,
    SDLK_LSUPER,
    SDLK_RSUPER,
    SDLK_MODE,
    SDLK_COMPOSE,
    SDLK_HELP,
    SDLK_PRINT,
    SDLK_SYSREQ,
    SDLK_BREAK,
    SDLK_MENU,
    SDLK_POWER,
    SDLK_EURO,
    SDLK_UNDO,
    SDLK_LAST,
    ...
} SDLKey;

typedef enum {
    KMOD_NONE,
    KMOD_LSHIFT,
    KMOD_RSHIFT,
    KMOD_LCTRL,
    KMOD_RCTRL,
    KMOD_LALT,
    KMOD_RALT,
    KMOD_LMETA,
    KMOD_RMETA,
    KMOD_NUM,
    KMOD_CAPS,
    KMOD_MODE,
    KMOD_RESERVED,
    ...
} SDLMod;

#define KMOD_CTRL ...
#define KMOD_SHIFT ...
#define KMOD_ALT ...
#define KMOD_META ...
""")

_sdl_keys = ffi.verify(
    include_dirs=['/usr/include/SDL', '/usr/local/include/SDL'],
    source="""
    #include <SDL_keysym.h>
    """
)

K_UNKNOWN = _sdl_keys.SDLK_UNKNOWN
K_FIRST = _sdl_keys.SDLK_FIRST
K_BACKSPACE = _sdl_keys.SDLK_BACKSPACE
K_TAB = _sdl_keys.SDLK_TAB
K_CLEAR = _sdl_keys.SDLK_CLEAR
K_RETURN = _sdl_keys.SDLK_RETURN
K_PAUSE = _sdl_keys.SDLK_PAUSE
K_ESCAPE = _sdl_keys.SDLK_ESCAPE
K_SPACE = _sdl_keys.SDLK_SPACE
K_EXCLAIM = _sdl_keys.SDLK_EXCLAIM
K_QUOTEDBL = _sdl_keys.SDLK_QUOTEDBL
K_HASH = _sdl_keys.SDLK_HASH
K_DOLLAR = _sdl_keys.SDLK_DOLLAR
K_AMPERSAND = _sdl_keys.SDLK_AMPERSAND
K_QUOTE = _sdl_keys.SDLK_QUOTE
K_LEFTPAREN = _sdl_keys.SDLK_LEFTPAREN
K_RIGHTPAREN = _sdl_keys.SDLK_RIGHTPAREN
K_ASTERISK = _sdl_keys.SDLK_ASTERISK
K_PLUS = _sdl_keys.SDLK_PLUS
K_COMMA = _sdl_keys.SDLK_COMMA
K_MINUS = _sdl_keys.SDLK_MINUS
K_PERIOD = _sdl_keys.SDLK_PERIOD
K_SLASH = _sdl_keys.SDLK_SLASH
K_0 = _sdl_keys.SDLK_0
K_1 = _sdl_keys.SDLK_1
K_2 = _sdl_keys.SDLK_2
K_3 = _sdl_keys.SDLK_3
K_4 = _sdl_keys.SDLK_4
K_5 = _sdl_keys.SDLK_5
K_6 = _sdl_keys.SDLK_6
K_7 = _sdl_keys.SDLK_7
K_8 = _sdl_keys.SDLK_8
K_9 = _sdl_keys.SDLK_9
K_COLON = _sdl_keys.SDLK_COLON
K_SEMICOLON = _sdl_keys.SDLK_SEMICOLON
K_LESS = _sdl_keys.SDLK_LESS
K_EQUALS = _sdl_keys.SDLK_EQUALS
K_GREATER = _sdl_keys.SDLK_GREATER
K_QUESTION = _sdl_keys.SDLK_QUESTION
K_AT = _sdl_keys.SDLK_AT
K_LEFTBRACKET = _sdl_keys.SDLK_LEFTBRACKET
K_BACKSLASH = _sdl_keys.SDLK_BACKSLASH
K_RIGHTBRACKET = _sdl_keys.SDLK_RIGHTBRACKET
K_CARET = _sdl_keys.SDLK_CARET
K_UNDERSCORE = _sdl_keys.SDLK_UNDERSCORE
K_BACKQUOTE = _sdl_keys.SDLK_BACKQUOTE
K_a = _sdl_keys.SDLK_a
K_b = _sdl_keys.SDLK_b
K_c = _sdl_keys.SDLK_c
K_d = _sdl_keys.SDLK_d
K_e = _sdl_keys.SDLK_e
K_f = _sdl_keys.SDLK_f
K_g = _sdl_keys.SDLK_g
K_h = _sdl_keys.SDLK_h
K_i = _sdl_keys.SDLK_i
K_j = _sdl_keys.SDLK_j
K_k = _sdl_keys.SDLK_k
K_l = _sdl_keys.SDLK_l
K_m = _sdl_keys.SDLK_m
K_n = _sdl_keys.SDLK_n
K_o = _sdl_keys.SDLK_o
K_p = _sdl_keys.SDLK_p
K_q = _sdl_keys.SDLK_q
K_r = _sdl_keys.SDLK_r
K_s = _sdl_keys.SDLK_s
K_t = _sdl_keys.SDLK_t
K_u = _sdl_keys.SDLK_u
K_v = _sdl_keys.SDLK_v
K_w = _sdl_keys.SDLK_w
K_x = _sdl_keys.SDLK_x
K_y = _sdl_keys.SDLK_y
K_z = _sdl_keys.SDLK_z
K_DELETE = _sdl_keys.SDLK_DELETE
K_WORLD_0 = _sdl_keys.SDLK_WORLD_0
K_WORLD_1 = _sdl_keys.SDLK_WORLD_1
K_WORLD_2 = _sdl_keys.SDLK_WORLD_2
K_WORLD_3 = _sdl_keys.SDLK_WORLD_3
K_WORLD_4 = _sdl_keys.SDLK_WORLD_4
K_WORLD_5 = _sdl_keys.SDLK_WORLD_5
K_WORLD_6 = _sdl_keys.SDLK_WORLD_6
K_WORLD_7 = _sdl_keys.SDLK_WORLD_7
K_WORLD_8 = _sdl_keys.SDLK_WORLD_8
K_WORLD_9 = _sdl_keys.SDLK_WORLD_9
K_WORLD_10 = _sdl_keys.SDLK_WORLD_10
K_WORLD_11 = _sdl_keys.SDLK_WORLD_11
K_WORLD_12 = _sdl_keys.SDLK_WORLD_12
K_WORLD_13 = _sdl_keys.SDLK_WORLD_13
K_WORLD_14 = _sdl_keys.SDLK_WORLD_14
K_WORLD_15 = _sdl_keys.SDLK_WORLD_15
K_WORLD_16 = _sdl_keys.SDLK_WORLD_16
K_WORLD_17 = _sdl_keys.SDLK_WORLD_17
K_WORLD_18 = _sdl_keys.SDLK_WORLD_18
K_WORLD_19 = _sdl_keys.SDLK_WORLD_19
K_WORLD_20 = _sdl_keys.SDLK_WORLD_20
K_WORLD_21 = _sdl_keys.SDLK_WORLD_21
K_WORLD_22 = _sdl_keys.SDLK_WORLD_22
K_WORLD_23 = _sdl_keys.SDLK_WORLD_23
K_WORLD_24 = _sdl_keys.SDLK_WORLD_24
K_WORLD_25 = _sdl_keys.SDLK_WORLD_25
K_WORLD_26 = _sdl_keys.SDLK_WORLD_26
K_WORLD_27 = _sdl_keys.SDLK_WORLD_27
K_WORLD_28 = _sdl_keys.SDLK_WORLD_28
K_WORLD_29 = _sdl_keys.SDLK_WORLD_29
K_WORLD_30 = _sdl_keys.SDLK_WORLD_30
K_WORLD_31 = _sdl_keys.SDLK_WORLD_31
K_WORLD_32 = _sdl_keys.SDLK_WORLD_32
K_WORLD_33 = _sdl_keys.SDLK_WORLD_33
K_WORLD_34 = _sdl_keys.SDLK_WORLD_34
K_WORLD_35 = _sdl_keys.SDLK_WORLD_35
K_WORLD_36 = _sdl_keys.SDLK_WORLD_36
K_WORLD_37 = _sdl_keys.SDLK_WORLD_37
K_WORLD_38 = _sdl_keys.SDLK_WORLD_38
K_WORLD_39 = _sdl_keys.SDLK_WORLD_39
K_WORLD_40 = _sdl_keys.SDLK_WORLD_40
K_WORLD_41 = _sdl_keys.SDLK_WORLD_41
K_WORLD_42 = _sdl_keys.SDLK_WORLD_42
K_WORLD_43 = _sdl_keys.SDLK_WORLD_43
K_WORLD_44 = _sdl_keys.SDLK_WORLD_44
K_WORLD_45 = _sdl_keys.SDLK_WORLD_45
K_WORLD_46 = _sdl_keys.SDLK_WORLD_46
K_WORLD_47 = _sdl_keys.SDLK_WORLD_47
K_WORLD_48 = _sdl_keys.SDLK_WORLD_48
K_WORLD_49 = _sdl_keys.SDLK_WORLD_49
K_WORLD_50 = _sdl_keys.SDLK_WORLD_50
K_WORLD_51 = _sdl_keys.SDLK_WORLD_51
K_WORLD_52 = _sdl_keys.SDLK_WORLD_52
K_WORLD_53 = _sdl_keys.SDLK_WORLD_53
K_WORLD_54 = _sdl_keys.SDLK_WORLD_54
K_WORLD_55 = _sdl_keys.SDLK_WORLD_55
K_WORLD_56 = _sdl_keys.SDLK_WORLD_56
K_WORLD_57 = _sdl_keys.SDLK_WORLD_57
K_WORLD_58 = _sdl_keys.SDLK_WORLD_58
K_WORLD_59 = _sdl_keys.SDLK_WORLD_59
K_WORLD_60 = _sdl_keys.SDLK_WORLD_60
K_WORLD_61 = _sdl_keys.SDLK_WORLD_61
K_WORLD_62 = _sdl_keys.SDLK_WORLD_62
K_WORLD_63 = _sdl_keys.SDLK_WORLD_63
K_WORLD_64 = _sdl_keys.SDLK_WORLD_64
K_WORLD_65 = _sdl_keys.SDLK_WORLD_65
K_WORLD_66 = _sdl_keys.SDLK_WORLD_66
K_WORLD_67 = _sdl_keys.SDLK_WORLD_67
K_WORLD_68 = _sdl_keys.SDLK_WORLD_68
K_WORLD_69 = _sdl_keys.SDLK_WORLD_69
K_WORLD_70 = _sdl_keys.SDLK_WORLD_70
K_WORLD_71 = _sdl_keys.SDLK_WORLD_71
K_WORLD_72 = _sdl_keys.SDLK_WORLD_72
K_WORLD_73 = _sdl_keys.SDLK_WORLD_73
K_WORLD_74 = _sdl_keys.SDLK_WORLD_74
K_WORLD_75 = _sdl_keys.SDLK_WORLD_75
K_WORLD_76 = _sdl_keys.SDLK_WORLD_76
K_WORLD_77 = _sdl_keys.SDLK_WORLD_77
K_WORLD_78 = _sdl_keys.SDLK_WORLD_78
K_WORLD_79 = _sdl_keys.SDLK_WORLD_79
K_WORLD_80 = _sdl_keys.SDLK_WORLD_80
K_WORLD_81 = _sdl_keys.SDLK_WORLD_81
K_WORLD_82 = _sdl_keys.SDLK_WORLD_82
K_WORLD_83 = _sdl_keys.SDLK_WORLD_83
K_WORLD_84 = _sdl_keys.SDLK_WORLD_84
K_WORLD_85 = _sdl_keys.SDLK_WORLD_85
K_WORLD_86 = _sdl_keys.SDLK_WORLD_86
K_WORLD_87 = _sdl_keys.SDLK_WORLD_87
K_WORLD_88 = _sdl_keys.SDLK_WORLD_88
K_WORLD_89 = _sdl_keys.SDLK_WORLD_89
K_WORLD_90 = _sdl_keys.SDLK_WORLD_90
K_WORLD_91 = _sdl_keys.SDLK_WORLD_91
K_WORLD_92 = _sdl_keys.SDLK_WORLD_92
K_WORLD_93 = _sdl_keys.SDLK_WORLD_93
K_WORLD_94 = _sdl_keys.SDLK_WORLD_94
K_WORLD_95 = _sdl_keys.SDLK_WORLD_95
K_KP0 = _sdl_keys.SDLK_KP0
K_KP1 = _sdl_keys.SDLK_KP1
K_KP2 = _sdl_keys.SDLK_KP2
K_KP3 = _sdl_keys.SDLK_KP3
K_KP4 = _sdl_keys.SDLK_KP4
K_KP5 = _sdl_keys.SDLK_KP5
K_KP6 = _sdl_keys.SDLK_KP6
K_KP7 = _sdl_keys.SDLK_KP7
K_KP8 = _sdl_keys.SDLK_KP8
K_KP9 = _sdl_keys.SDLK_KP9
K_KP_PERIOD = _sdl_keys.SDLK_KP_PERIOD
K_KP_DIVIDE = _sdl_keys.SDLK_KP_DIVIDE
K_KP_MULTIPLY = _sdl_keys.SDLK_KP_MULTIPLY
K_KP_MINUS = _sdl_keys.SDLK_KP_MINUS
K_KP_PLUS = _sdl_keys.SDLK_KP_PLUS
K_KP_ENTER = _sdl_keys.SDLK_KP_ENTER
K_KP_EQUALS = _sdl_keys.SDLK_KP_EQUALS
K_UP = _sdl_keys.SDLK_UP
K_DOWN = _sdl_keys.SDLK_DOWN
K_RIGHT = _sdl_keys.SDLK_RIGHT
K_LEFT = _sdl_keys.SDLK_LEFT
K_INSERT = _sdl_keys.SDLK_INSERT
K_HOME = _sdl_keys.SDLK_HOME
K_END = _sdl_keys.SDLK_END
K_PAGEUP = _sdl_keys.SDLK_PAGEUP
K_PAGEDOWN = _sdl_keys.SDLK_PAGEDOWN
K_F1 = _sdl_keys.SDLK_F1
K_F2 = _sdl_keys.SDLK_F2
K_F3 = _sdl_keys.SDLK_F3
K_F4 = _sdl_keys.SDLK_F4
K_F5 = _sdl_keys.SDLK_F5
K_F6 = _sdl_keys.SDLK_F6
K_F7 = _sdl_keys.SDLK_F7
K_F8 = _sdl_keys.SDLK_F8
K_F9 = _sdl_keys.SDLK_F9
K_F10 = _sdl_keys.SDLK_F10
K_F11 = _sdl_keys.SDLK_F11
K_F12 = _sdl_keys.SDLK_F12
K_F13 = _sdl_keys.SDLK_F13
K_F14 = _sdl_keys.SDLK_F14
K_F15 = _sdl_keys.SDLK_F15
K_NUMLOCK = _sdl_keys.SDLK_NUMLOCK
K_CAPSLOCK = _sdl_keys.SDLK_CAPSLOCK
K_SCROLLOCK = _sdl_keys.SDLK_SCROLLOCK
K_RSHIFT = _sdl_keys.SDLK_RSHIFT
K_LSHIFT = _sdl_keys.SDLK_LSHIFT
K_RCTRL = _sdl_keys.SDLK_RCTRL
K_LCTRL = _sdl_keys.SDLK_LCTRL
K_RALT = _sdl_keys.SDLK_RALT
K_LALT = _sdl_keys.SDLK_LALT
K_RMETA = _sdl_keys.SDLK_RMETA
K_LMETA = _sdl_keys.SDLK_LMETA
K_LSUPER = _sdl_keys.SDLK_LSUPER
K_RSUPER = _sdl_keys.SDLK_RSUPER
K_MODE = _sdl_keys.SDLK_MODE
K_COMPOSE = _sdl_keys.SDLK_COMPOSE
K_HELP = _sdl_keys.SDLK_HELP
K_PRINT = _sdl_keys.SDLK_PRINT
K_SYSREQ = _sdl_keys.SDLK_SYSREQ
K_BREAK = _sdl_keys.SDLK_BREAK
K_MENU = _sdl_keys.SDLK_MENU
K_POWER = _sdl_keys.SDLK_POWER
K_EURO = _sdl_keys.SDLK_EURO
K_UNDO = _sdl_keys.SDLK_UNDO

KMOD_NONE = _sdl_keys.KMOD_NONE
KMOD_LSHIFT = _sdl_keys.KMOD_LSHIFT
KMOD_RSHIFT = _sdl_keys.KMOD_RSHIFT
KMOD_LCTRL = _sdl_keys.KMOD_LCTRL
KMOD_RCTRL = _sdl_keys.KMOD_RCTRL
KMOD_LALT = _sdl_keys.KMOD_LALT
KMOD_RALT = _sdl_keys.KMOD_RALT
KMOD_LMETA = _sdl_keys.KMOD_LMETA
KMOD_RMETA = _sdl_keys.KMOD_RMETA
KMOD_NUM = _sdl_keys.KMOD_NUM
KMOD_CAPS = _sdl_keys.KMOD_CAPS
KMOD_MODE = _sdl_keys.KMOD_MODE
KMOD_CTRL = _sdl_keys.KMOD_CTRL
KMOD_SHIFT = _sdl_keys.KMOD_SHIFT
KMOD_ALT = _sdl_keys.KMOD_ALT
KMOD_META = _sdl_keys.KMOD_META

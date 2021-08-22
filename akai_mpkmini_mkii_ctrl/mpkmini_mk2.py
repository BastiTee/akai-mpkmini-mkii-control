# -*- coding: utf-8 -*-
r"""Construct for MPKmini MK2 Patch data.

Source: https://github.com/mungewell/mpd-utils/blob/master/mpk_mini.py
"""

from construct import (Array, Byte, Computed, Const, Default, Embedded, Enum,
                       ExprAdapter, Int16ub, Sequence, Struct, obj_)

# -----------------------------------------------------------------------------
# CONSTANTS DEFINING MPK FEATURES
# -----------------------------------------------------------------------------

_PADS = 8
_PBANKS = 2
_PTOTAL = _PADS * _PBANKS

_DIALS = 8
_DBANKS = 1
_DTOTAL = _DIALS * _DBANKS

# -----------------------------------------------------------------------------
# DEFINE FILE FORMAT USING CONSTRUCT (V2.9)
# https://github.com/construct/construct
# -----------------------------------------------------------------------------

General = Struct(
    'preset' / Byte,
    'pchannel' / Byte,              # Pads
    'dchannel' / Byte,              # Dials and Keys

    'octave' / Enum(
        Byte,
        OCT_M4=0,
        OCT_M3=1,
        OCT_M2=2,
        OCT_M1=3,
        OCT_0=4,
        OCT_P1=5,
        OCT_P2=6,
        OCT_P3=7,
        OCT_P4=8,
    ),
)

Arpeggio_enable = Struct(
    'enable' / Default(Enum(
        Byte,
        OFF=0,
        ON=1,
    ), 0),
)
Arpeggio_mode = Struct(
    'mode' / Enum(
        Byte,
        UP=0,
        DOWN=1,
        EXCLUSIVE=2,
        INCLUSIVE=3,
        RANDOM=4,
        ORDER=5,
    ),
)
Arpeggio_div = Struct(
    'division' / Enum(
        Byte,
        DIV_1_4=0,
        DIV_1_4T=1,
        DIV_1_8=2,
        DIV_1_8T=3,
        DIV_1_16=4,
        DIV_1_16T=5,
        DIV_1_32=6,
        DIV_1_32T=7,
    ),
)
Arpeggio_clk = Struct(
    'clock' / Enum(
        Byte,
        INTERNAL=0,
        EXTERNAL=1,
    ),
)
Arpeggio = Struct(
    'latch' / Enum(
        Byte,
        DISABLE=0,
        ENABLE=1,
    ),
    'swing' / Enum(
        Byte,
        SWING_50=0,
        SWING_55=1,
        SWING_57=2,
        SWING_59=3,
        SWING_61=4,
        SWING_64=5,
    ),
    'taps' / Byte,
    'tempo' / ExprAdapter(
        Int16ub,  # 7bit stuffed - each byte max 0x7F
        ((obj_ & 0x7f) + ((obj_ & 0x7f00) >> 1)),
        ((obj_ & 0x7f) + ((obj_ & 0x3f80) << 1)),
    ),
    'octaves' / Enum(
        Byte,
        OCT_1=0,
        OCT_2=1,
        OCT_3=2,
        OCT_4=3,
    ),
)

Joy = Struct(                       # Default values allow Mk1->Mk2 conversion
    'axis_x' / Default(Enum(
        Byte,
        PBEND=0,
        CC1=1,
        CC2=2,
    ), 0),
    'x_up' / Default(Byte, 0),
    'x_down' / Default(Byte, 1),    # CC2 only
    'axis_y' / Default(Enum(
        Byte,
        PBEND=0,
        CC1=1,
        CC2=2,
    ), 1),
    'y_up' / Default(Byte, 1),
    'y_down' / Default(Byte, 1),    # CC2 only
)

Pad = Struct(
    'note' / Byte,
    'prog' / Byte,
    'midicc' / Byte,
    'trigger' / Enum(
        Byte,          # MidiCC Only
        MOMENTARY=0,
        TOGGLE=1,
    ),
)

Dial = Struct(
    'midicc' / Byte,
    'min' / Byte,
    'max' / Byte,
)

Transpose = Struct(                 # Default values allow Mk1->Mk2 conversion
    'transpose' / Default(Enum(
        Byte,
        TRANS_M12=0,
        TRANS_M11=1,
        TRANS_M10=2,
        TRANS_M9=3,
        TRANS_M8=4,
        TRANS_M7=5,
        TRANS_M6=6,
        TRANS_M5=7,
        TRANS_M4=8,
        TRANS_M3=9,
        TRANS_M2=10,
        TRANS_M1=11,
        TRANS_0=12,
        TRANS_P1=13,
        TRANS_P2=14,
        TRANS_P3=15,
        TRANS_P4=16,
        TRANS_P5=17,
        TRANS_P6=18,
        TRANS_P7=19,
        TRANS_P8=20,
        TRANS_P9=21,
        TRANS_P10=22,
        TRANS_P11=23,
        TRANS_P12=24,
    ), 12),
)

Empty = Struct(                     # Hack for Mk1 -> MK2 conversion
)

Footer = Struct(
    Const(b'\xf7'),                 # SysEx End
)

Header_Mk2 = Struct(
    'mk2' / Computed(True),

    Const(b'\xf0'),                 # SysEx Begin
    Const(b'\x47\x00'),             # Mfg ID = Akai
    Const(b'\x26'),                 # Dev ID = MPK Mk2
    Const(b'\x64'),                 # CMD = Dump (67) / Load (64) Preset
    Const(b'\x00\x6d'),             # Len = 109bytes (7bit stuffed)

    Embedded(General),              # Note: different order to Mk1
    Embedded(Arpeggio_enable),
    Embedded(Arpeggio_mode),
    Embedded(Arpeggio_div),
    Embedded(Arpeggio_clk),
    Embedded(Arpeggio),
    Embedded(Joy),
)

MPK_MINI_MK2 = Sequence(
    Header_Mk2,
    Array(_PBANKS, Array(_PADS, Pad,)),
    Array(_DBANKS, Array(_DIALS, Dial,)),
    Transpose,
    Footer,
)

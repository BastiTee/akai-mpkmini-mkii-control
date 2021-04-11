#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""First experiment for a single patch roundtrip."""

from pathlib import Path
from time import sleep
from typing import Any, Tuple

import rtmidi
from rtmidi import midiutil
from akai_mpkmini_mkii_ctrl.mpk_mini import Mpk_mk2

MPKMINI_DEVICE = 'MPK Mini Mk II'


def main() -> None:  # noqa: D103
    # Create temp folder
    Path('output').mkdir(exist_ok=True)

    # Setup MIDI receiver
    midi_in, midi_in_port_name = midiutil.open_midiinput(0)
    midi_in.ignore_types(sysex=False)  # !! Otherwise no sysex receiver
    midi_in.set_callback(MidiInputHandler(midi_in_port_name))

    # Setup output
    midi_out = rtmidi.MidiOut()
    midi_out.open_port(0)

    # Check that we're actually connected with an AKAI MPKmini MK2
    assert midi_in_port_name == MPKMINI_DEVICE
    assert midi_out.get_port_name(0) == MPKMINI_DEVICE

    # Send sysex to fetch patch 1
    sysex = 'F0 47 00 26 66 00 01 03 F7'
    data = bytearray.fromhex(sysex)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    print(f'- SENT {len(data)} BYTES. SYSEX = "{sysex}"...')

    try:
        # Main application loop
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        midi_in.close_port()
        midi_out.close_port()


class MidiInputHandler(object):  # noqa: D101

    def __init__(  # noqa: D107
        self,
        port: str
    ) -> None:
        self.port = port

    def __call__(  # noqa: D102
        self,
        event: Tuple[Any, Any],
        data: Any = None
    ) -> None:
        msg_dec, deltatime = event
        msg_hex = [hex(m) for m in msg_dec]
        print(f'- RECEIVED {len(msg_dec)} BYTES')
        print(f'DEC = {" ".join([str(m) for m in msg_dec])}')
        print(f'HEX = {" ".join([str(m)[2:].zfill(2) for m in msg_hex])}')

        config = Mpk_mk2.parse(bytearray(msg_dec))
        print(config)

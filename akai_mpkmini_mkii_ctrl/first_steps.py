#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""First experiment for a single patch roundtrip."""

import binascii
from time import sleep
from typing import List, Sequence, Tuple

import rtmidi
from rtmidi import MidiIn, MidiOut, midiutil

from akai_mpkmini_mkii_ctrl.mpk_mini import Mpk_mk2
from akai_mpkmini_mkii_ctrl.note_converter import note_to_decimal as n2d


def main() -> None:  # noqa: D103
    # Create temp folder
    midi_in, midi_out = setup_midi_in_and_out()

    set_patch_to_defaults(midi_in, midi_out)

    midi_in.close_port()
    midi_out.close_port()


def set_patch_to_defaults(  # noqa: D103
    midi_in: MidiIn,
    midi_out: MidiOut
) -> None:
    config = get_config_from_device(1, midi_in, midi_out)

    # MIDI channels
    config[0].pchannel = 1  # Pads on channel 2
    config[0].dchannel = 1  # Dials and keys on channel 2

    # Key centers
    config[0].octave = 4  # Octave center (4 = middle)
    config[3].transpose = 'TRANS_0'  # Transpose value (note-wise shift)

    # Arpeggiator
    config[0].enable = 'OFF'
    config[0].mode = 'EXCLUSIVE'
    config[0].division = 'DIV_1_8'
    config[0].clock = 'INTERNAL'
    config[0].latch = 'DISABLE'
    config[0].swing = 'SWING_50'
    config[0].taps = 3
    config[0].tempo = 140
    config[0].octaves = 'OCT_1'

    # Joystick
    config[0].axis_x = 'CC2'
    config[0].x_up = 1
    config[0].x_down = 1
    config[0].axis_y = 'PBEND'
    config[0].y_up = 0
    config[0].y_down = 1

    current_cc = 12  # Start with CC 4 upwards
    current_prog_change = 20  # Start with PROG 20 upwards
    for bank in range(0, 2):
        for pad in range(0, 8):
            config[1][bank][pad].midicc = current_cc
            config[1][bank][pad].prog = current_prog_change
            # CC-MODE Momentary (0) or Trigger (1)
            config[1][bank][pad].trigger = 0
            current_cc += 1
            current_prog_change += 1

    # BANK A
    config[1][0][4].note = n2d('c1')
    config[1][0][5].note = n2d('c#1')
    config[1][0][6].note = n2d('f#1')
    config[1][0][7].note = n2d('a#1')

    config[1][0][0].note = n2d('d1')
    config[1][0][1].note = n2d('e1')
    config[1][0][2].note = n2d('g1')
    config[1][0][3].note = n2d('a1')

    # BANK B
    config[1][1][4].note = n2d('c1')
    config[1][1][5].note = n2d('c#1')
    config[1][1][6].note = n2d('f#1')
    config[1][1][7].note = n2d('a#1')

    config[1][1][0].note = n2d('d1')
    config[1][1][1].note = n2d('e1')
    config[1][1][2].note = n2d('g1')
    config[1][1][3].note = n2d('a1')

    # MIDI CC dials
    current_cc = 4  # Start with CC 4 upwards
    for dial in config[2][0]:
        dial.min = 0
        dial.max = 127
        dial.midicc = current_cc
        current_cc += 1

    send_config_to_device(config, 0, midi_out)


def __update_and_sleep(
    config: Mpk_mk2,
    midi_out: MidiOut
) -> None:
    send_config_to_device(config, 0, midi_out)
    sleep(1.0)


def wait_for_sysex_response(  # noqa: D103
    midi_in: MidiIn
) -> Tuple[List[int], Sequence]:
    message = None
    while True:
        raw_tuple = midi_in.get_message()
        if raw_tuple:
            message = raw_tuple[0]
            break
        sleep(0.01)
    # assert len(message) == 117
    assert message[4] == 103
    # Flip 4-th position from DEC 103 (HEX 67) to DEC 100 (HEX 64)
    # to flip patch from 'Receive' to 'Send'
    message[4] = 100
    message_hex = [hex(m) for m in message]
    print(f'DEC = {" ".join([str(m) for m in message])}')
    print(f'HEX = {" ".join([str(m)[2:].zfill(2) for m in message_hex])}')
    return message, Mpk_mk2.parse(bytearray(message))


def send_sysex_from_binary_file(  # noqa: D103
    file_path: str,
    midi_out: MidiOut
) -> None:
    with open(file_path, 'rb') as in_file_byte:
        data = in_file_byte.read(2000)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    print(f'- SENT {len(data)} BYTES. SYSEX = "{data_hex}"...')


def send_sysex_from_hex_string(  # noqa: D103
    hex_string: str,
    midi_out: MidiOut
) -> None:
    data = bytearray.fromhex(hex_string)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    print(f'- SENT {len(data)} BYTES. SYSEX = "{data_hex}"...')


def setup_midi_in_and_out() -> Tuple[MidiIn, MidiOut]:  # noqa: D103
    device_name = 'MPK Mini Mk II'

    # Setup output
    midi_out = rtmidi.MidiOut()
    midi_out.open_port(0)

    # Setup MIDI receiver
    midi_in, midi_in_port_name = midiutil.open_midiinput(0)
    midi_in.ignore_types(sysex=False)  # !! Otherwise no sysex receiver

    # Check that we're actually connected with an AKAI MPKmini MK2
    assert midi_in_port_name == device_name
    assert midi_out.get_port_name(0) == device_name

    return midi_in, midi_out


def get_config_from_device(  # noqa: D103
    preset: int,  # 0 = RAM, 1-4 Stored Presets
    midi_in: MidiIn,
    midi_out: MidiOut
) -> Mpk_mk2:
    assert preset >= 0 and preset <= 4
    send_sysex_from_hex_string(f'f0 47 00 26 66 00 01 0{preset} f7', midi_out)
    _, config = wait_for_sysex_response(midi_in)
    return config


def send_config_to_device(  # noqa: D103
    config: Mpk_mk2,
    preset: int,  # 0 = RAM, 1-4 Stored Presets
    midi_out: MidiOut
) -> None:
    assert preset >= 0 and preset <= 4
    config[0].preset = preset
    print('-----------')
    print(config)
    print('-----------')
    data = Mpk_mk2.build(config)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    print(f'- SENT {len(data)} BYTES. SYSEX = "{data_hex}"...')

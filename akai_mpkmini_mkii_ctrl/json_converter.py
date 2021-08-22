# -*- coding: utf-8 -*-
r"""Convert JSON presets to Construct presets."""

import logging
from os import path
from re import sub
from typing import Any, List

from akai_mpkmini_mkii_ctrl.mpkmini_mk2 import MPK_MINI_MK2
from akai_mpkmini_mkii_ctrl.note_converter import note_to_decimal as n2d

TEMPLATE = path.join(path.dirname(path.abspath(__file__)), 'preset.mk2')


def json_to_binary(json: dict) -> List[int]:
    # TODO I don't know how to initialise the 'MPK_MINI_MK2' structure
    # manually without a bunch of boilerplate. So I load some from file.
    preset = MPK_MINI_MK2.parse_file(TEMPLATE)

    # Constants
    preset[0].mk2 = True  # TODO This is obsolete
    preset[0].preset = 0  # Will be changed depending on the --patch option

    # Midi channel for pads and dials/keys
    preset[0].pchannel = __read_json(json, 'midi-channels.pads', 1) - 1
    preset[0].dchannel = __read_json(json, 'midi-channels.keys', 1) - 1

    # Octave-wise shift
    preset[0].octave = __read_json(json, 'transponse.octave', 'OCT_0')
    # Note-wise shift
    preset[3].transpose = __read_json(json, 'transponse.note', 'TRANS_0')

    # Arpeggiator
    preset[0].enable = __read_json(json, 'arpeggiator.enable', 'OFF')
    preset[0].mode = __read_json(json, 'arpeggiator.mode', 'EXCLUSIVE')
    preset[0].division = __read_json(json, 'arpeggiator.division', 'DIV_1_8')
    preset[0].clock = __read_json(json, 'arpeggiator.clock', 'INTERNAL')
    preset[0].latch = __read_json(json, 'arpeggiator.latch', 'DISABLE')
    preset[0].swing = __read_json(json, 'arpeggiator.swing', 'SWING_50')
    preset[0].taps = __read_json(json, 'arpeggiator.taps', 3)
    preset[0].tempo = __read_json(json, 'arpeggiator.tempo', 140)
    preset[0].octaves = __read_json(json, 'arpeggiator.octaves', 'OCT_1')

    # Joystick
    preset[0].axis_x = __read_json(json, 'joystick.axis-x', 'CC2')
    preset[0].x_up = __read_json(json, 'joystick.x-up', 1)
    preset[0].x_down = __read_json(json, 'joystick.x-down', 1)
    preset[0].axis_y = __read_json(json, 'joystick.axis-y', 'PBEND')
    preset[0].y_up = __read_json(json, 'joystick.y-up', 0)
    preset[0].y_down = __read_json(json, 'joystick.y-down', 1)

    # CC and Prog Change setup for pads
    current_cc = 12  # Start with CC 12 upwards
    current_prog_change = 20  # Start with PROG 20 upwards
    for bank in range(0, 2):
        for pad in range(0, 8):
            preset[1][bank][pad].midicc = current_cc
            preset[1][bank][pad].prog = current_prog_change
            # CC-MODE Momentary (0) or Trigger (1)
            preset[1][bank][pad].trigger = 0
            current_cc += 1
            current_prog_change += 1

    # MIDI CC Dials
    dials_cc = __extract_bank_int(json, 'dials.cc', '4 5 6 7 8 9 10 11')
    for i, dial in enumerate(preset[2][0]):
        dial.min = __read_json(json, 'dials.min-value', 0)
        dial.max = __read_json(json, 'dials.max-value', 0)
        dial.midicc = dials_cc[i]

    # Pad Banks
    for entry in enumerate(['bank-a', 'bank-b']):
        notes = __extract_bank_notes(json, f'pads.{entry[1]}.notes')
        cc = __extract_bank_int(
            json, f'pads.{entry[1]}.cc', '20 21 22 23 24 25 26 27'
        )
        prog = __extract_bank_int(
            json, f'pads.{entry[1]}.prog', '20 21 22 23 24 25 26 27'
        )
        trigger = __extract_bank_trigger(
            json, f'pads.{entry[1]}.trigger', 'M M M M M M M M'
        )
        for pad in range(0, 8):
            preset[1][entry[0]][pad].note = n2d(notes[pad])
            preset[1][entry[0]][pad].midicc = cc[pad]
            preset[1][entry[0]][pad].prog = prog[pad] - 1
            preset[1][entry[0]][pad].trigger = trigger[pad]

    logging.debug(preset)

    # Finalise
    data = MPK_MINI_MK2.build(preset)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    return data


def __extract_bank_notes(json: dict, path: str) -> List[str]:
    default_bank_notes = '- - - - - - - -'  # i.e. by default set to C-2
    # Extract notes from preset path
    notes = [
        note.strip()
        for note in __read_json(json, path, default_bank_notes).split(r' ')
    ]
    logging.debug(f'{path} = {notes}')
    # Replace default value '-' with 'C-2'
    return [sub(r'^-$', 'C-2', note) for note in notes]


def __extract_bank_int(json: dict, path: str, default_bank: str) -> List[int]:
    int_string = __read_json(json, path, default_bank)
    ints = [int(value.strip()) for value in int_string.split(' ')]
    logging.debug(f'{path} = {ints}')
    return ints


def __extract_bank_trigger(
    json: dict, path: str, default_bank: str
) -> List[str]:
    trigger_string = __read_json(json, path, default_bank)
    trigger = []
    for t in trigger_string.split(' '):
        if t == 'T':
            trigger.append('TOGGLE')
        elif t == 'M':
            trigger.append('MOMENTARY')
        else:
            raise ValueError('Only T and M is supported')
    logging.debug(f'{path} = {trigger}')
    return trigger


def __read_json(json: dict, path: str, default_value: Any) -> Any:
    if not path:
        return default_value
    json = json if json else {}
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        value = json if json else default_value
        logging.debug(f'JSON | {path} = {value}')
        return value
    except KeyError:
        logging.warn(f'!!! JSON | {path} = {default_value} '
                     + '(Key not found. Default will be used.)')
        return default_value

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Convert JSON presets to Construct presets.

TODO This does not yet convert all possible values from JSON ¯\_(ツ)_/¯
But refer to resources/json-presets/default.json and this code to extend it.
"""

from os import path
from typing import Any, List

from akai_mpkmini_mkii_ctrl.mpkmini_mk2 import MPK_MINI_MK2
from akai_mpkmini_mkii_ctrl.note_converter import note_to_decimal as n2d

TEMPLATE = path.join(path.dirname(path.abspath(__file__)), 'preset.mk2')


def json_to_binary(json: dict) -> List[int]:
    preset = MPK_MINI_MK2.parse_file(TEMPLATE)
    # Defaults
    preset[0].mk2 = True
    preset[0].preset = 0
    # Midi channel for pads
    preset[0].pchannel = json_lookup(json, 'midi-channels.pads', 0)
    # Midi channel for dials and keys
    preset[0].dchannel = json_lookup(json, 'midi-channels.keys', 0)
    # Octave-wise shift
    preset[0].octave = json_lookup(json, 'transponse.octave', 'OCT_0')
    # Note-wise shift
    preset[3].transpose = json_lookup(json, 'transponse.note', 'TRANS_0')
    # Arpeggiator
    preset[0].enable = 'OFF'
    preset[0].mode = 'EXCLUSIVE'
    preset[0].division = 'DIV_1_8'
    preset[0].clock = 'INTERNAL'
    preset[0].latch = 'DISABLE'
    preset[0].swing = 'SWING_50'
    preset[0].taps = 3
    preset[0].tempo = 140
    preset[0].octaves = 'OCT_1'
    # Joystick
    preset[0].axis_x = 'CC2'
    preset[0].x_up = 1
    preset[0].x_down = 1
    preset[0].axis_y = 'PBEND'
    preset[0].y_up = 0
    preset[0].y_down = 1
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
    current_cc = 4  # Start with CC 4 upwards
    for dial in preset[2][0]:
        dial.min = 0
        dial.max = 127
        dial.midicc = current_cc
        current_cc += 1
    # BANK A Notes
    bank_a_notes = __extract_bank_notes(json, 'pads.bank-a.notes')
    preset[1][0][0].note = n2d(bank_a_notes[0])
    preset[1][0][1].note = n2d(bank_a_notes[1])
    preset[1][0][2].note = n2d(bank_a_notes[2])
    preset[1][0][3].note = n2d(bank_a_notes[3])
    preset[1][0][4].note = n2d(bank_a_notes[4])
    preset[1][0][5].note = n2d(bank_a_notes[5])
    preset[1][0][6].note = n2d(bank_a_notes[6])
    preset[1][0][7].note = n2d(bank_a_notes[7])
    # BANK B Notes
    bank_b_notes = __extract_bank_notes(json, 'pads.bank-b.notes')
    preset[1][1][0].note = n2d(bank_b_notes[0])
    preset[1][1][1].note = n2d(bank_b_notes[1])
    preset[1][1][2].note = n2d(bank_b_notes[2])
    preset[1][1][3].note = n2d(bank_b_notes[3])
    preset[1][1][4].note = n2d(bank_b_notes[4])
    preset[1][1][5].note = n2d(bank_b_notes[5])
    preset[1][1][6].note = n2d(bank_b_notes[6])
    preset[1][1][7].note = n2d(bank_b_notes[7])

    print(preset)

    data = MPK_MINI_MK2.build(preset)
    assert data[0] == 0xF0 and data[-1] == 0xF7

    return data


def __extract_bank_notes(json: dict, path: str) -> List[str]:
    return [note.strip() for note in json_lookup(
        json, path, 'C1 C#1 D1 D#1 E1 F1 F#1 G1'
    ).split(r' ')]


def json_lookup(json: dict, path: str, default_value: Any) -> Any:
    if not path:
        return default_value
    json = json if json else {}
    try:
        for breadcrumb in path.split('.'):
            json = json[breadcrumb]
        return json if json else default_value
    except KeyError:
        return default_value

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Midi controller."""

import binascii
from contextlib import contextmanager
from time import sleep
from typing import Generator, List, Sequence, Tuple

import click
import rtmidi
from rtmidi import MidiIn, MidiOut, midiutil

from akai_mpkmini_mkii_ctrl.mpkmini_mk2 import MPK_MINI_MK2

DEVICE_NAME = 'MPK Mini Mk II'


@contextmanager
def midi_connection(
) -> Generator[Tuple[MidiIn, MidiOut], None, None]:
    midi_in, midi_out = setup_midi_in_and_out()
    try:
        yield (midi_in, midi_out)
    finally:
        midi_in.close_port()
        midi_out.close_port()


def wait_for_sysex_response(
    midi_in: MidiIn
) -> Tuple[List[int], Sequence]:
    message = None
    while True:
        raw_tuple = midi_in.get_message()
        if raw_tuple:
            message = raw_tuple[0]
            break
        sleep(0.01)
    assert len(message) == 117
    assert message[4] == 103
    # Flip 4-th position from DEC 103 (HEX 67) to DEC 100 (HEX 64)
    # to flip patch from 'Receive' to 'Send'
    message[4] = 100
    message_hex = ''.join([str(hex(m))[2:].zfill(2) for m in message])
    __print(f'- RECEIVED {len(message)} BYTES. SYSEX:\n{message_hex}')
    return message, MPK_MINI_MK2.parse(bytearray(message))


def send_sysex_from_binary_file(
    file_path: str,
    midi_out: MidiOut
) -> None:
    with open(file_path, 'rb') as in_file_byte:
        data = in_file_byte.read(2000)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    __print(f'- SENT {len(data)} BYTES. SYSEX:\n{data_hex}')


def send_sysex_from_hex_string(
    hex_string: str,
    midi_out: MidiOut
) -> None:
    data = bytearray.fromhex(hex_string)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    __print(f'- SENT {len(data)} BYTES. SYSEX:\n{data_hex}')


def setup_midi_in_and_out() -> Tuple[MidiIn, MidiOut]:

    # Setup output
    midi_out = rtmidi.MidiOut()
    midi_out.open_port(0)

    # Setup MIDI receiver
    midi_in, midi_in_port_name = midiutil.open_midiinput(0)
    midi_in.ignore_types(sysex=False)  # !! Otherwise no sysex receiver

    # Check that we're actually connected with an AKAI MPKmini MK2
    assert midi_in_port_name == DEVICE_NAME
    assert midi_out.get_port_name(0) == DEVICE_NAME

    return midi_in, midi_out


def get_config_from_device(
    preset: int,  # 0 = RAM, 1-4 Stored Presets
    midi_in: MidiIn,
    midi_out: MidiOut
) -> MPK_MINI_MK2:
    assert preset >= 0 and preset <= 4
    send_sysex_from_hex_string(f'f0 47 00 26 66 00 01 0{preset} f7', midi_out)
    _, config = wait_for_sysex_response(midi_in)
    return config


def send_config_to_device(
    config: MPK_MINI_MK2,
    preset: int,  # 0 = RAM, 1-4 Stored Presets
    midi_out: MidiOut
) -> None:
    assert preset >= 0 and preset <= 4
    config[0].preset = preset
    data = MPK_MINI_MK2.build(config)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    __print(f'- SENT {len(data)} BYTES. SYSEX:\n{data_hex}')


def __print(message: str) -> None:
    if click.get_current_context().obj['verbose']:
        print(message)

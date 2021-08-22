# -*- coding: utf-8 -*-
r"""Midi controller."""

import binascii
from contextlib import contextmanager
from time import sleep
from typing import Generator, List, Tuple

import click
import rtmidi
from rtmidi import MidiIn, MidiOut, RtMidiError, midiutil

from akai_mpkmini_mkii_ctrl.mpkmini_mk2 import MPK_MINI_MK2

DEVICE_NAME = 'MPK Mini Mk II'


@contextmanager
def midi_connection(
    midi_port: int
) -> Generator[Tuple[MidiIn, MidiOut], None, None]:
    midi_in, midi_out = setup_midi_in_and_out(midi_port)
    try:
        yield (midi_in, midi_out)
    finally:
        midi_in.close_port()
        midi_out.close_port()


def setup_midi_in_and_out(midi_port: int) -> Tuple[MidiIn, MidiOut]:
    # Setup MIDI sender
    midi_out = rtmidi.MidiOut()
    try:
        midi_out.open_port(midi_port)
    except RtMidiError as err:
        __error('Cannot connect to MIDI device.', err)
    midi_out_port_name = midi_out.get_port_name(midi_port)

    # Setup MIDI receiver
    midi_in, midi_in_port_name = midiutil.open_midiinput(midi_port)
    midi_in.ignore_types(sysex=False)  # !! Otherwise no sysex receiver

    # Check that we're actually connected with an AKAI MPKmini MK2
    if midi_in_port_name != DEVICE_NAME:
        __error(f'Input device not of type "{DEVICE_NAME}" '
                + f'but "{midi_in_port_name}"')
    if midi_out_port_name != DEVICE_NAME:
        __error(f'Output device not of type "{DEVICE_NAME}" '
                + f'but "{midi_out_port_name}"')

    return midi_in, midi_out


def send_binary_to_device(
    file_path: str,
    preset: int,
    midi_out: MidiOut
) -> None:
    with open(file_path, 'rb') as in_file_byte:
        data = in_file_byte.read(2000)
    config = MPK_MINI_MK2.parse(data)
    send_config_to_device(config, preset, midi_out)


def send_config_to_device(
    config: MPK_MINI_MK2,
    preset: int,
    midi_out: MidiOut
) -> None:
    config[0].preset = preset
    data = MPK_MINI_MK2.build(config)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    __print(f'- SENT {len(data)} BYTES. SYSEX:\n{data_hex}')


def get_binary_from_device(
    preset: int,
    midi_in: MidiIn,
    midi_out: MidiOut
) -> List[int]:
    send_sysex_from_hex_string(f'f0 47 00 26 66 00 01 0{preset} f7', midi_out)
    return receive_sysex(midi_in)


def get_config_from_device(
    preset: int,
    midi_in: MidiIn,
    midi_out: MidiOut
) -> MPK_MINI_MK2:
    message = get_binary_from_device(preset, midi_in, midi_out)
    return MPK_MINI_MK2.parse(bytearray(message))


def send_sysex_from_hex_string(
    hex_string: str,
    midi_out: MidiOut
) -> None:
    data = bytearray.fromhex(hex_string)
    assert data[0] == 0xF0 and data[-1] == 0xF7
    midi_out.send_message(data)
    data_hex = str(binascii.hexlify(bytearray(data)), 'utf-8')
    __print(f'- SENT {len(data)} BYTES. SYSEX:\n{data_hex}')


def receive_sysex(
    midi_in: MidiIn
) -> List[int]:
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
    return message


def __print(message: str) -> None:
    if click.get_current_context().obj['verbose']:
        print(message)


def __error(message: str, err: Exception = None) -> None:
    if err:
        print(f'!!! {message}: {err}\n')
    else:
        print(f'!!! {message}\n')
    print(click.get_current_context().get_help())
    exit(1)

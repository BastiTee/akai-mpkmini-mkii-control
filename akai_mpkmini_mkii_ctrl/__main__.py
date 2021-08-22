# -*- coding: utf-8 -*-
r"""Command-line controller for AKAI MPKmini MK2."""


import collections.abc
from json import dumps, load
from typing import List

import click

from akai_mpkmini_mkii_ctrl import controller as ctrl
from akai_mpkmini_mkii_ctrl import json_converter
from akai_mpkmini_mkii_ctrl.mpkmini_mk2 import MPK_MINI_MK2


def __update(d: dict, u: collections.abc.Mapping) -> dict:
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = __update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


@click.group(help=__doc__)
@click.option(
    '--preset', '-p', required=True, metavar='NUM',
    type=click.Choice(['0', '1', '2', '3', '4']), default='0',
    help='Target preset slot (0 = RAM, 1-4 = Stored preset)'
)
@click.option(
    '--midi-port', '-m', required=True, metavar='NUM',
    type=click.INT, default=0,
    help='MIDI port (0 = Omni, > 0 = Specific MIDI port)'
)
@click.option(
    '--verbose', '-v', is_flag=True,
    help='Verbose output'
)
@click.pass_context
def main(
    ctx: click.Context,
    preset: str,
    midi_port: str,
    verbose: bool
) -> None:
    ctx.ensure_object(dict)
    ctx.obj['preset'] = int(preset)
    ctx.obj['midi_port'] = int(midi_port)
    ctx.obj['verbose'] = verbose


@main.command(help='Print preset on device in human readable format')
@click.pass_context
def print_preset(ctx: click.Context) -> None:
    with ctrl.midi_connection(ctx.obj['midi_port']) as (m_in, m_out):
        config = ctrl.get_config_from_device(ctx.obj['preset'], m_in, m_out)
        print(config)


@main.command(help='Push a local binary preset to the device')
@click.option(
    '--input-file', '-i', required=True, metavar='FILE',
    help='Binary input file, i.e., a regular *.mk2 preset file'
)
@click.pass_context
def push_preset(
    ctx: click.Context,
    input_file: str
) -> None:
    with ctrl.midi_connection(ctx.obj['midi_port']) as (m_in, m_out):
        ctrl.send_binary_to_device(
            input_file, ctx.obj['preset'], m_out
        )


@main.command(help='Push a local JSON preset to the device')
@click.option(
    '--input-file', '-i', required=True, metavar='FILE',
    help='JSON input file', multiple=True
)
@click.option(
    '--check', '-c', is_flag=True, help='Check resulting JSON before pushing'
)
@click.pass_context
def push_json_preset(
    ctx: click.Context,
    input_file: List[str],
    check: bool
) -> None:
    # Combine all provided JSON files
    json_data: dict = {}
    for in_file in input_file:
        with open(in_file, 'r') as in_file_handle:
            json_preset = load(in_file_handle)
        __update(json_data, json_preset)
    if check:
        print(dumps(json_data, indent=4))
        input('Press key to continue...')
    # Convert to binary structure
    binary = json_converter.json_to_binary(json_data)
    config = MPK_MINI_MK2.parse(binary)
    with ctrl.midi_connection(ctx.obj['midi_port']) as (m_in, m_out):
        ctrl.send_config_to_device(config, ctx.obj['preset'], m_out)


@main.command(help='Pull a binary from the device and write to file')
@click.option(
    '--output-file', '-o', required=True, metavar='FILE',
    help='Binary output file, i.e., a regular *.mk2 preset file'
)
@click.pass_context
def pull_preset(
    ctx: click.Context,
    output_file: str
) -> None:
    with ctrl.midi_connection(ctx.obj['midi_port']) as (m_in, m_out):
        binary = ctrl.get_binary_from_device(ctx.obj['preset'], m_in, m_out)
        with open(output_file, 'wb') as output_file_handle:
            output_file_handle.write(bytes(binary))


if __name__ == '__main__':
    main()

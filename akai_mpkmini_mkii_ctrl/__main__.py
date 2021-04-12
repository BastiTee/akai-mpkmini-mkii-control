# -*- coding: utf-8 -*-
"""Command-line controller for AKAI MPKmini MK2."""


from json import load

import click

from akai_mpkmini_mkii_ctrl import controller as ctrl
from akai_mpkmini_mkii_ctrl import json_converter


@click.group(help=__doc__)
@click.option(
    '--preset', '-p', required=True, metavar='NUM',
    type=click.Choice(['0', '1', '2', '3', '4']), default='0',
    help='Preset selector (0 = RAM, 1-4 Stored preset)'
)
@click.option(
    '--midi-port', '-m', required=True, metavar='NUM',
    type=click.INT, default=0, help='MIDI port'
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


@main.command(help='Print preset in human readable format')
@click.pass_context
def print_preset(ctx: click.Context) -> None:
    with ctrl.midi_connection(ctx.obj['midi_port']) as (m_in, m_out):
        config = ctrl.get_config_from_device(ctx.obj['preset'], m_in, m_out)
        print(config)


@main.command(help='Push a binary preset from file to the device')
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


@main.command(help='Converts a JSON-based preset to a binary preset')
@click.option(
    '--input-file', '-i', required=True, metavar='FILE',
    help='JSON input file'
)
@click.option(
    '--output-file', '-o', required=True, metavar='FILE',
    help='Binary output file, i.e., a regular *.mk2 preset file'
)
@click.pass_context
def convert(
    ctx: click.Context,
    input_file: str,
    output_file: str
) -> None:
    with open(input_file, 'r') as input_file_handle:
        json_data = load(input_file_handle)
        binary = json_converter.json_to_binary(json_data)
        with open(output_file, 'wb') as output_file_handle:
            output_file_handle.write(bytes(binary))


if __name__ == '__main__':
    main()

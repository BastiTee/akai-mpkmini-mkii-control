# -*- coding: utf-8 -*-
"""Command-line controller for AKAI MPKmini MK2."""


import click

from akai_mpkmini_mkii_ctrl import controller as ctrl


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


if __name__ == '__main__':
    main()


# def set_patch_to_defaults(
#     midi_in: MidiIn,
#     midi_out: MidiOut
# ) -> None:
#     config = get_config_from_device(1, midi_in, midi_out)

#     # MIDI channels
#     config[0].pchannel = 1  # Pads on channel 2
#     config[0].dchannel = 1  # Dials and keys on channel 2

#     # Key centers
#     config[0].octave = 4  # Octave center (4 = middle)
#     config[3].transpose = 'TRANS_0'  # Transpose value (note-wise shift)

#     # Arpeggiator
#     config[0].enable = 'OFF'
#     config[0].mode = 'EXCLUSIVE'
#     config[0].division = 'DIV_1_8'
#     config[0].clock = 'INTERNAL'
#     config[0].latch = 'DISABLE'
#     config[0].swing = 'SWING_50'
#     config[0].taps = 3
#     config[0].tempo = 140
#     config[0].octaves = 'OCT_1'

#     # Joystick
#     config[0].axis_x = 'CC2'
#     config[0].x_up = 1
#     config[0].x_down = 1
#     config[0].axis_y = 'PBEND'
#     config[0].y_up = 0
#     config[0].y_down = 1

#     current_cc = 12  # Start with CC 4 upwards
#     current_prog_change = 20  # Start with PROG 20 upwards
#     for bank in range(0, 2):
#         for pad in range(0, 8):
#             config[1][bank][pad].midicc = current_cc
#             config[1][bank][pad].prog = current_prog_change
#             # CC-MODE Momentary (0) or Trigger (1)
#             config[1][bank][pad].trigger = 0
#             current_cc += 1
#             current_prog_change += 1

#     # BANK A
#     config[1][0][4].note = n2d('C1')
#     config[1][0][5].note = n2d('C#1')
#     config[1][0][6].note = n2d('F#1')
#     config[1][0][7].note = n2d('A#1')

#     config[1][0][0].note = n2d('E2')
#     config[1][0][1].note = n2d('E1')
#     config[1][0][2].note = n2d('G1')
#     config[1][0][3].note = n2d('A1')

#     # BANK B
#     config[1][1][4].note = n2d('C1')
#     config[1][1][5].note = n2d('C#1')
#     config[1][1][6].note = n2d('F#1')
#     config[1][1][7].note = n2d('A#1')

#     config[1][1][0].note = n2d('D1')
#     config[1][1][1].note = n2d('E1')
#     config[1][1][2].note = n2d('G1')
#     config[1][1][3].note = n2d('A1')

#     # MIDI CC dials
#     current_cc = 4  # Start with CC 4 upwards
#     for dial in config[2][0]:
#         dial.min = 0
#         dial.max = 127
#         dial.midicc = current_cc
#         current_cc += 1

#     send_config_to_device(config, 0, midi_out)

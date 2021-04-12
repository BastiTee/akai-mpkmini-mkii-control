# Command-line controller for AKAI MPKmini MK II

[![CI](https://github.com/BastiTee/akai-mpkmini-mkii-control/actions/workflows/main.yml/badge.svg)](https://github.com/BastiTee/akai-mpkmini-mkii-control/actions/workflows/main.yml)

Best effort project to overcome the fact that AKAI doesn't seem to be interested in fixing Segmentation faults in their [MPKmini Editor](https://www.akaipro.com/mpk-mini-mkii). For questions reach out to <http://twitter.com/basti_tee>

## Install

```
make install
```

## Usage

```
Usage: akai_mpkmini_mkii_ctrl [OPTIONS] COMMAND [ARGS]...

  Command-line controller for AKAI MPKmini MK2.

Options:
  -p, --preset NUM     Preset selector (0 = RAM, 1-4 Stored preset)
                       [required]

  -m, --midi-port NUM  MIDI port  [required]
  -v, --verbose        Verbose output
  --help               Show this message and exit.

Commands:
  convert       Converts a JSON-based preset to a binary preset
  print-preset  Print preset in human readable format
  pull-preset   Pull a binary from the device and write to file
  push-preset   Push a binary preset from file to the device
```

Print preset stored on program 1 in human readable format:

```shell
python3 -m akai_mpkmini_mkii_ctrl --preset 1 print-preset
```

Download preset stored in RAM to a local file:

```shell
python3 -m akai_mpkmini_mkii_ctrl --preset 0 pull-preset --output-file ram-preset.mk2
```

Upload preset from somewhere to program 2 (also works with factory presets):

```shell
python3 -m akai_mpkmini_mkii_ctrl --preset 2 push-preset --input-file resources/factory-patches/preset1.mk2
```

Experimental: Create a preset using a [JSON-based definition](resources/json-presets/default.json) file:

```shell
python3 -m akai_mpkmini_mkii_ctrl convert --input-file resources/json-presets/default.json --output-file resources/json-presets/default.mk2
```

## Sources

- <https://github.com/gljubojevic/akai-mpk-mini-editor>
- <https://github.com/mungewell/mpd-utils>
- <https://www.snoize.com/midimonitor/>
- <https://github.com/gbevin/SendMIDI>
- <https://github.com/gbevin/ReceiveMIDI>
- <https://www.akaipro.com/mpk-mini-mkii>

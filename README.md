# Command-line controller for AKAI MPKmini MK II

![MPKmini picture](resources/gfx/akai-picture.jpeg)

[Source](https://commons.wikimedia.org/wiki/File:Akai_MPK_mini_MK2_-_angled_left_-_2014_NAMM_Show_(by_Matt_Vanacoro).jpg) – [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/deed.en)

[![CI](https://github.com/BastiTee/akai-mpkmini-mkii-control/actions/workflows/main.yml/badge.svg)](https://github.com/BastiTee/akai-mpkmini-mkii-control/actions/workflows/main.yml)

Best effort project to overcome the fact that AKAI doesn't seem to be interested in fixing Segmentation faults in their [MPKmini Editor](https://www.akaipro.com/mpk-mini-mkii). For questions reach out to <http://twitter.com/basti_tee>.

It is currently mostly fixing my own itches but it would be a pleasure to find like-minded people who would like to contribute :)

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
  convert           Converts a JSON-based preset to a binary preset
  print-preset      Print preset in human readable format
  pull-preset       Pull a binary from the device and write to file
  push-json-preset  Push a JSON preset from file to the device
  push-preset       Push a binary preset from file to the device
```

Print preset stored on program 1 in human readable format:

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 1 print-preset
```

Download preset stored in RAM to a local file:

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 0 \
pull-preset \
--output-file ram-preset.mk2
```

Upload preset from somewhere to program 2 (also works with factory binary presets):

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 2 \
push-preset \
--input-file resources/factory-patches/preset1.mk2
```

Experimental: Create a preset using a [JSON-based definition](resources/json-presets/Logic-Base.json) file:

```shell
python3 -m akai_mpkmini_mkii_ctrl \
push-json-preset \
--input-file resources/json-presets/Logic-Base.json \
--input-file resources/json-presets/Logic-RetroSynth+Juno.json \
--output-file resources/json-presets/default.mk2
```

Note that you are able to add up several input files in order for easier re-use.

## Sources

- <https://github.com/gljubojevic/akai-mpk-mini-editor>
- <https://github.com/mungewell/mpd-utils>
- <https://www.snoize.com/midimonitor/>
- <https://github.com/gbevin/SendMIDI>
- <https://github.com/gbevin/ReceiveMIDI>
- <https://www.akaipro.com/mpk-mini-mkii>

## Todos & ideas

- [x] JSON-patch support for all possible options
- [ ] Removal of obsolete MPK_MINI_MK2.mk2 property
- [ ] User-centric versus developer-centric usage documentation
- [ ] Publish to pypi
- [ ] Binary executables for Mac

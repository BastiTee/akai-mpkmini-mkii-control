# Command-line controller for AKAI MPKmini MK II

![](resources/gfx/akai-picture.jpeg)

[Source](https://commons.wikimedia.org/wiki/File:Akai_MPK_mini_MK2_-_angled_left_-_2014_NAMM_Show_(by_Matt_Vanacoro).jpg) – [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/deed.en)

[![CI](https://github.com/BastiTee/akai-mpkmini-mkii-control/actions/workflows/main.yml/badge.svg)](https://github.com/BastiTee/akai-mpkmini-mkii-control/actions/workflows/main.yml) ![PyPU - Version](https://img.shields.io/pypi/v/akai-mpkmini-mkii-ctrl.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/akai-mpkmini-mkii-ctrl.svg)

Best effort project to overcome the fact that AKAI doesn't seem to be interested in fixing Segmentation faults in their [MPKmini Editor](https://www.akaipro.com/mpk-mini-mkii).

It currently fixes my own itches but I gladly accept feedback!

## Install

To install via [PyPi](https://pypi.org/project/akai-mpkmini-mkii-ctrl/):

```
pip3 install --user akai-mpkmini-mkii-ctrl
```

Please note that the dependency `python-rtmidi` requires compilation resources to be present on your system. For Debian-like systems for example you need to install `sudo apt-get install libasound2-dev`. Refer to the [project documentation](https://spotlightkid.github.io/python-rtmidi/installation.html) for details.

To install from source you can use:

- `python3 setup.py install`, or
- `make install` which will run a `pipenv` including linting, tests, etc.

## Usage

`akai_mpkmini_mkii_ctrl` supports a set of commands to push or pull presets to and from the device. All commands have a common set of options:

```
-p, --preset NUM     Target preset slot (0 = RAM, 1-4 = Stored preset)
-m, --midi-port NUM  MIDI port (0 = Omni, > 0 = Specific MIDI port)
-v, --verbose        Verbose output
--help               Show this message and exit.
```

### Commands

`print-preset`: Print preset on device in human readable format. In this example it will print the preset stored in slot 1 on the device.

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 1 print-preset
```

`pull-preset`: Pull a binary from the device and write to file.

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 0 \
pull-preset \
--output-file ram-preset.mk2
```

`push-preset`: Push a local binary preset to the device. This also works with [factory binary presets](resources/factory-patches).

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 2 \
push-preset \
--input-file resources/factory-patches/preset1.mk2
```

`push-json-preset`: Push a local JSON preset ([Example](resources/json-presets/Logic-Base.json)) to the device. Notice that you are able to combine several input files for easier re-use. The configurations are applied in order, e.g., in this case [`Logic-Base.json`](resources/json-presets/Logic-Base.json) will be extended with the properties found in [`Logic-RetroSynth+Juno.json`](resources/json-presets/Logic-RetroSynth+Juno.json).

```shell
python3 -m akai_mpkmini_mkii_ctrl \
--preset 0 \
push-json-preset \
--input-file resources/json-presets/Logic-Base.json \
--input-file resources/json-presets/Logic-RetroSynth+Juno.json
```

## Development

You can prepare a `pipenv`-based development environment using:

```shell
make clean venv
```

You can also install the controller to your system using:

```shell
make install
```

To use the local `pipenv`-based version you can use the following command from where you cloned the repository:

```shell
pipenv run python akai_mpkmini_mkii_ctrl
```

## Resources

The implementation is based upon the following resources:

- <https://github.com/gljubojevic/akai-mpk-mini-editor>
- <https://github.com/mungewell/mpd-utils>
- <https://www.snoize.com/midimonitor/>
- <https://github.com/gbevin/SendMIDI>
- <https://github.com/gbevin/ReceiveMIDI>
- <https://www.akaipro.com/mpk-mini-mkii>

# Command-line controller for AKAI MPKmini MK II

## Notes

### Knowledge

- <https://github.com/gljubojevic/akai-mpk-mini-editor>
- <https://cycling74.com/forums/akai-mpk-mini-send-get-signals-to-light-buttons>
- <https://www.gearslutz.com/board/electronic-music-instruments-and-electronic-music-production/1330121-can-anyone-help-how-create-sysex-file-hex-message.html>

### Applications

- <https://github.com/mungewell/mpd-utils>
- <https://www.akaipro.com/mpk-mini-mkii>
- <https://www.snoize.com/midimonitor/>
- <https://github.com/gbevin/SendMIDI/releases>
- <https://github.com/gbevin/ReceiveMIDI>
- <https://www.snoize.com/sysexlibrarian/docs.html>

## Reverse Engineering

```
F0 47 7F 7C 63 00 01 01 F7

F0 47 00 26 66 00 01 01 F7

-- GET PROG 1

To MPK Mini Mk II SysEx Akai 9 bytes F0 47 00 26 66 00 01 01 F7 17:39:59.149
From MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 67 00 6D 01 01 01 03 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 28 00 14 00 29...

To MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 64 00 6D 01 01 01 03 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 28 00 14 00 29...

-- GET PROG 2

To MPK Mini Mk II SysEx Akai 9 bytes F0 47 00 26 66 00 01 02 F7
From MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 67 00 6D 02 01 01 03 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 24 00 14 00 25...

To MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 64 00 6D 02 01 01 03 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 24 00 14 00 25...

-- GET PROG 3

To MPK Mini Mk II SysEx Akai 9 bytes F0 47 00 26 66 00 01 03 F7
From MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 67 00 6D 03 01 01 00 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 04 00 14 01 05...

To MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 64 00 6D 03 01 01 00 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 04 00 14 01 05...

-- GET PROG 4

To MPK Mini Mk II SysEx Akai 9 bytes F0 47 00 26 66 00 01 04 F7
From MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 67 00 6D 04 01 01 00 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 2C 00 14 01 2D...

To MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 64 00 6D 04 01 01 00 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 2C 00 14 01 2D...

SEND TO RAM

To MPK Mini Mk II SysEx Akai 117 bytes F0 47 00 26 64 00 6D 00 01 01 00 00 00 04 00 00 00 03 00 78 00 00 00 01 02 01 01 2C 00 14 01 2D...
```

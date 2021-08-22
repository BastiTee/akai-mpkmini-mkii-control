# -*- coding: utf-8 -*-
r"""Convert notes to and from decimal."""

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note_to_decimal(note: str) -> int:
    try:
        if not note or not isinstance(note, str):
            raise ValueError
        note_split, oct_split = (
            (note[:2].upper(), note[2:]) if '#' in note else
            (note[:1].upper(), note[1:])
        )
        note_idx = NOTES.index(note_split)
        oct_idx = int(oct_split)
        if oct_idx < -2 or oct_idx > 8:
            raise ValueError
        note_idx = note_idx + (12 * (oct_idx + 2))
        if note_idx > 127:
            raise ValueError
    except ValueError:
        raise ValueError(f'Note "{note}" unknown.')
    return note_idx


def decimal_to_note(decimal: int) -> str:
    if (
        decimal is None
        or not isinstance(decimal, int)
        or decimal < 0
        or decimal > 127
    ):
        raise ValueError(f'Decimal "{decimal}" unknown.')
    note = NOTES[decimal % 12]
    octave = int(((decimal - (decimal % 12)) / 12) - 2)
    return f'{note}{octave}'

# -*- coding: utf-8 -*-
r"""Basic test suite."""

import __future__  # noqa: F401

import pytest

from akai_mpkmini_mkii_ctrl import note_converter


class TestNoteConverter:  # noqa: D101

    @pytest.mark.parametrize('from_note, to_dec', [
        ('C-2', 0),
        ('C5', 84),
        ('G8', 127)
    ])
    def test_note_to_decimal(self, from_note: str, to_dec: int) -> None:
        actual: int = note_converter.note_to_decimal(from_note)
        assert actual == to_dec

    @pytest.mark.parametrize('from_dec, to_note', [
        (0, 'C-2'),
        (84, 'C5'),
        (127, 'G8')
    ])
    def test_decimal_to_note(self, from_dec: int, to_note: str) -> None:
        actual: str = note_converter.decimal_to_note(from_dec)
        assert actual == to_note

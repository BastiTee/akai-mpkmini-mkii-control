# -*- coding: utf-8 -*-
r"""Test suite for akai_mpkmini_mkii_ctrl.note_converter."""

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

    @pytest.mark.parametrize('from_note', [
        None, '', 'X#1', 'A8', 'B-3'
    ])
    def test_note_to_decimal_exceptions(self, from_note: str) -> None:
        with pytest.raises(ValueError, match=r'Note .* unknown'):
            note_converter.note_to_decimal(from_note)

    @pytest.mark.parametrize('from_dec, to_note', [
        (0, 'C-2'),
        (84, 'C5'),
        (127, 'G8')
    ])
    def test_decimal_to_note(self, from_dec: int, to_note: str) -> None:
        actual: str = note_converter.decimal_to_note(from_dec)
        assert actual == to_note

    @pytest.mark.parametrize('from_dec', [
        None, -1, 128, 1000
    ])
    def test_decimal_to_note_exceptions(self, from_dec: int) -> None:
        with pytest.raises(ValueError, match=r'Decimal .* unknown'):
            note_converter.decimal_to_note(from_dec)

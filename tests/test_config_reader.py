# -*- coding: utf-8 -*-
r"""Test suite for akai_mpkmini_mkii_ctrl.note_converter."""

from os import path

import pytest

from akai_mpkmini_mkii_ctrl.config_reader import load_config_from_file

FIXTURES = path.join(path.dirname(__file__), 'fixtures')
JSON_CONFIG = path.join(FIXTURES, 'json-config.json')
YAML_CONFIG = path.join(FIXTURES, 'yaml-config.yaml')
HTML_CONFIG = path.join(FIXTURES, 'html.html')


class TestConfigReader:  # noqa: D101

    def test_load_config_from_missing_file(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_config_from_file('')

    def test_load_config_with_unsupported_format(self) -> None:
        with pytest.raises(ValueError) as ve:
            load_config_from_file(HTML_CONFIG)
        assert 'Unsupported configuration file format' in str(ve)

    def test_load_config_from_json_file(self) -> None:
        config: dict = load_config_from_file(JSON_CONFIG)
        TestConfigReader.__assert_content(config)

    def test_load_config_from_yaml_file(self) -> None:
        config: dict = load_config_from_file(YAML_CONFIG)
        TestConfigReader.__assert_content(config)

    @staticmethod
    def __assert_content(config: dict) -> None:
        assert config
        assert config['midi-channels']['pads'] == 2
        assert config['transponse']['octave'] == 'OCT_0'
        assert config['arpeggiator']['enable'] == 'OFF'
        assert config['joystick']['axis-x'] == 'CC2'
        assert config['dials']['min-value'] == 0
        assert config['dials']['min-value'] == 0
        assert config['pads']['bank-a']['cc'] == '20 21 22 23 24 25 26 27'
        assert config['pads']['bank-b']['prog'] == '9 10 11 12 13 14 15 16'

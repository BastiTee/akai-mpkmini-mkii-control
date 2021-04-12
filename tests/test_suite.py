# -*- coding: utf-8 -*-
"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__  # noqa: F401

import json  # noqa: F401
from os import path  # noqa: F401
from re import IGNORECASE, sub  # noqa: F401

import pytest
import requests  # noqa: F401

import akai_mpkmini_mkii_ctrl  # noqa: F401


class TestUtils:  # noqa: D101

    @pytest.mark.parametrize('number_left, number_right', [
        (None, 1), (1, None), (None, None)
    ])
    def test_dummy(
            self,
            number_left: int,
            number_right: int
    ) -> None:
        print(number_left, number_right)
        assert True

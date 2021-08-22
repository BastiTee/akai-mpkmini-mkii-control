# -*- coding: utf-8 -*-
r"""Basic test suite."""

import __future__  # noqa: F401

import pytest


class TestUtils:  # noqa: D101

    @pytest.mark.parametrize('number_left, number_right', [
        (None, 1), (1, None), (None, None)
    ])
    def test_dummy(
            self,
            number_left: int,
            number_right: int
    ) -> None:
        assert True

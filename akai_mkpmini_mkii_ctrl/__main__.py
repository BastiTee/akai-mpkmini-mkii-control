# -*- coding: utf-8 -*-
"""Module init-file.

A module's __name__ is set equal to '__main__' when read from standard input,
a script, or from an interactive prompt.
"""

from akai_mkpmini_mkii_ctrl.utils import add_two_numbers

print('Executed from command line...')
print(f'2 + 2 equals {add_two_numbers(2, 2)}')

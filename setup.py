#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup process."""

from io import open
from os import path

from setuptools import find_packages, setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'),
          encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Basic project information
    name='akai-mpkmini-mkii-ctrl',
    version='0.2.0',
    # Authorship and online reference
    author='Basti Tee',
    author_email='basti.tee@posteo.de',
    url='https://github.com/BastiTee/akai-mpkmini-mkii-control',
    # Detailled description
    description='Command-line controller for AKAI MPKmini MK II.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='sysex synth midi',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    # Package configuration
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    python_requires='>= 3.6',
    install_requires=[
        'python-rtmidi',
        'click',
        'construct<2.10'
    ],
    # Licensing and copyright
    license='Apache 2.0'
)

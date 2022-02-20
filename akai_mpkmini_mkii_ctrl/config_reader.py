# -*- coding: utf-8 -*-
r"""Configuration file reader."""

import collections.abc
from json import JSONDecodeError, load

import yaml


def load_config_from_file(file_path: str) -> dict:
    try:
        # Assuming JSON format...
        with open(file_path, 'r') as json_handle:
            return load(json_handle)
    except JSONDecodeError:
        pass

    try:
        # ... then YAML format
        with open(file_path, 'r') as yaml_handle:
            return yaml.safe_load(yaml_handle)
    except yaml.YAMLError:
        pass

    # ... and raise error if nothing was loadable.
    raise ValueError('Unsupported configuration file format')


def update_config(d: dict, u: collections.abc.Mapping) -> dict:
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_config(d.get(k, {}), v)
        else:
            d[k] = v
    return d

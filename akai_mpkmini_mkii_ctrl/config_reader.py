# -*- coding: utf-8 -*-
r"""Configuration file reader."""

import collections.abc
from json import JSONDecodeError, load

import yaml

UNSUPPORTED_ERROR = 'Unsupported configuration file format: '


def load_config_from_file(file_path: str) -> dict:
    try:
        # Assuming JSON format...
        with open(file_path, 'r') as json_handle:
            config_json: dict = load(json_handle)
            if not isinstance(config_json, dict):
                raise ValueError(f'{UNSUPPORTED_ERROR}{file_path}')
            return config_json
    except JSONDecodeError:
        pass

    try:
        # ... then YAML format
        with open(file_path, 'r') as yaml_handle:
            config_yml: dict = yaml.safe_load(yaml_handle)
            if not isinstance(config_yml, dict):
                raise ValueError(f'{UNSUPPORTED_ERROR}{file_path}')
            return config_yml
    except yaml.YAMLError:
        pass

    raise ValueError(f'{UNSUPPORTED_ERROR}{file_path}')


def update_config(d: dict, u: collections.abc.Mapping) -> dict:
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_config(d.get(k, {}), v)
        else:
            d[k] = v
    return d

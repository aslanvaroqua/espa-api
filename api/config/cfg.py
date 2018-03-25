""" Environment variables override default configurations from file """

import os
import configparser


def from_env(section):
    prefix = 'ESPA_API_{}_'.format(section.upper())
    return {k.split(prefix)[1]:v
            for k, v in os.environ.items() if k.startswith(prefix)}


def cfgfile(config_file=None):
    return config_file or os.getenv('ESPA_API_CONFIG_PATH',
                                    os.path.join(os.path.expanduser('~/.usgs'),
                                                 '.espa_api.ini'))


def from_file(section, config_file=None):
    if not os.path.exists(cfgfile(config_file)):
        return {}
    config = configparser.ConfigParser()
    config.read(cfgfile(config_file))
    return {opt.upper(): config.get(section, opt)
            for opt in config.options(section)}


def get(section, config_file=None, lower=False):
    return {k.lower() if lower else k: v for k, v in
            dict(from_file(section, config_file), **from_env(section)).items()}

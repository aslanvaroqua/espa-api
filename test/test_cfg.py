import os

import pytest

from api.config import cfg


def test_environ():
    os.environ['ESPA_API_DB_USERNAME'] = 'george'
    assert cfg.get('db')['USERNAME'] == 'george'
    assert 'username' in cfg.get('db', lower=True)

def test_config_not_found():
    os.environ['ESPA_API_CONFIG_PATH'] = '/path/to/nowhere'
    assert {} == cfg.get('db')
    assert 'path' in cfg.get('config', lower=True)

def test_local_config():
    os.environ['ESPA_API_CONFIG_PATH'] = './run/config.ini'
    assert 'key' in cfg.get('config', lower=True)

import os
import mock

import pytest

from api.config import cfg


@mock.patch.dict(os.environ, {'ESPA_API_DB_USERNAME': 'george'})
def test_environ():
    assert cfg.get('db')['USERNAME'] == 'george'
    assert 'username' in cfg.get('db', lower=True)

@mock.patch.dict(os.environ, {'ESPA_API_CONFIG_PATH': '/path/to/nowhere'})
def test_config_not_found():
    assert {} == cfg.get('db')
    assert 'path' in cfg.get('config', lower=True)

@mock.patch.dict(os.environ, {'ESPA_API_CONFIG_PATH': './run/config.ini'})
def test_local_config():
    assert 'key' in cfg.get('config', lower=True)

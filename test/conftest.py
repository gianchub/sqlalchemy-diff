import os

import pytest
import yaml


@pytest.fixture(scope="session")
def project_root():
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def test_config(project_root):
    config_file = os.path.join(project_root, "config", "config.yaml")
    with open(config_file) as stream:
        config = yaml.load(stream.read())
    return config


@pytest.fixture(scope="session")
def db_uri(test_config):
    return test_config['DB_URIS']['test']

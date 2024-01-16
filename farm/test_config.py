import farm
import pytest

@pytest.fixture(scope="session", autouse=True)
def logging_setup():
    farm.init_logs(True)
 
def test_config():
    config = farm.Config('config.json')
    assert config is not None
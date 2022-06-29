import pytest

from src.io.get_files_dict import main as get_files_dict


@pytest.fixture(scope='session')
def fixture_get_files_dict():
    return get_files_dict()

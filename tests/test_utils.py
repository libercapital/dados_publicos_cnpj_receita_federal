from src.io.utils import create_folder, check_if_folder_is_empty
from unittest.mock import Mock


def test_create_folder_that_exists(mocker):
    """
    Test must NOT call 'os.mkdir'
    :param mocker:
    :return:
    """
    mock_os = Mock()
    mocker.patch('src.io.utils.os', mock_os)
    mock_os.path.exists.return_value = True
    mock_os.makedirs.return_value = Mock()
    create_folder('bla')

    mock_os.makedirs.assert_not_called()


def test_create_folder_that_not_exists(mocker):
    """
    Test must call 'os.mkdir'
    :param mocker:
    :return:
    """
    mock_os = Mock()
    mocker.patch('src.io.utils.os', mock_os)
    mock_os.path.exists.return_value = False
    mock_os.makedirs.return_value = Mock()
    create_folder('bla')

    mock_os.makedirs.assert_called()


def test_create_folder_that_not_exists_subfolders(mocker):
    """
    Test must call 'os.mkdir'
    :param mocker:
    :return:
    """
    mock_os = Mock()
    mocker.patch('src.io.utils.os', mock_os)
    mock_os.path.exists.return_value = False
    mock_os.makedirs.return_value = Mock()
    create_folder('bla/bla1/bla2/bla3')

    mock_os.makedirs.assert_called()


def check_if_folder_is_empty_true(mocker):
    """
    Test must NOT call 'os.mkdir'
    :param mocker:
    :return:
    """
    mock_os = Mock()
    mocker.patch('src.io.utils.os', mock_os)
    mock_os.path.listdir.return_value = []
    folder_path = 'bla/bla1/bla2/bla3'
    is_empty = check_if_folder_is_empty(folder_path=folder_path)
    is_empty_expected = True
    assert is_empty == is_empty_expected


def check_if_folder_is_empty_false(mocker):
    """
    Test must NOT call 'os.mkdir'
    :param mocker:
    :return:
    """
    mock_os = Mock()
    mocker.patch('src.io.utils.os', mock_os)
    mock_os.path.listdir.return_value = ['a.zip', 'b.zip', 'c.zip']
    folder_path = 'bla/bla1/bla2/bla3'
    is_empty = check_if_folder_is_empty(folder_path=folder_path)
    is_empty_expected = False
    assert is_empty == is_empty_expected

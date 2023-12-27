from unittest.mock import Mock

from src.db_models.utils import check_pk_exists


def test_db_models_utils_check_pk_exists_true(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.execute_sql_cmd', mock_engine)
    mock_engine.return_value = [('pk1', 0)]

    return_expected = check_pk_exists(table_name='tbl1')

    assert return_expected


def test_db_models_utils_check_pk_exists_false(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.execute_sql_cmd', mock_engine)
    mock_engine.return_value = []

    return_expected = check_pk_exists(table_name='tbl1')

    assert return_expected is False

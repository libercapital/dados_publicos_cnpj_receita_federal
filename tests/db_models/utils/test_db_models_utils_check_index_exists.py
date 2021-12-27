from unittest.mock import Mock

from src.db_models.utils import check_index_exists


def test_db_models_utils_check_index_exists_idx_already_exits(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.settings.ENGINE', mock_engine)
    mock_engine.execute.return_value = [('idx', 0)]

    return_expected = check_index_exists(table_name='tbl1', idx='idx')
    sql = "SELECT indexname FROM pg_indexes WHERE tablename = 'tbl1'"
    mock_engine.execute.assert_called_with(sql)

    assert return_expected


def test_db_models_utils_check_index_exists_idx_already_exits_multiple(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.settings.ENGINE', mock_engine)
    mock_engine.execute.return_value = [('idx', 0), ('idx2', 0), ('idx3', 0), ('idx4', 0), ]

    return_expected = check_index_exists(table_name='tbl1', idx='idx4')
    sql = "SELECT indexname FROM pg_indexes WHERE tablename = 'tbl1'"
    mock_engine.execute.assert_called_with(sql)

    assert return_expected


def test_db_models_utils_check_index_exists_idx_not_exits(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.settings.ENGINE', mock_engine)
    mock_engine.execute.return_value = [('idx', 0)]

    return_expected = check_index_exists(table_name='tbl1', idx='idx2')
    sql = "SELECT indexname FROM pg_indexes WHERE tablename = 'tbl1'"
    mock_engine.execute.assert_called_with(sql)

    assert return_expected is False


def test_db_models_utils_check_index_exists_tbl_not_exits(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.settings.ENGINE', mock_engine)
    mock_engine.execute.return_value = []

    return_expected = check_index_exists(table_name='tbl2', idx='idx')
    sql = "SELECT indexname FROM pg_indexes WHERE tablename = 'tbl2'"
    mock_engine.execute.assert_called_with(sql)

    assert return_expected is False

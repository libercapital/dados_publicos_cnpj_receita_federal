from unittest.mock import Mock

from src.db_models.utils import delete_index


def test_db_models_utils_delete_index_can_delete(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.settings.ENGINE', mock_engine)
    mocker.patch('src.db_models.utils.check_index_exists', Mock(return_value=True))

    delete_index(table_name='tbl1', idx='idx')
    sql = "drop index idx"
    mock_engine.execute.assert_called_with(sql)


def test_db_models_utils_delete_index_can_not_delete(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.settings.ENGINE', mock_engine)
    mocker.patch('src.db_models.utils.check_index_exists', Mock(return_value=False))

    delete_index(table_name='tbl1', idx='idx')
    mock_engine.execute.assert_not_called()

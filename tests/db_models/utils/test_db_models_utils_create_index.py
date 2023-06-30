from src.db_models.utils import create_index
from unittest.mock import Mock


def test_db_models_utils_create_index_can_delete(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.execute_sql_cmd', mock_engine)
    mocker.patch('src.db_models.utils.check_index_exists', Mock(return_value=False))

    create_index(table_name='tbl1', idx='idx', column='c1')
    sql = "create index idx on tbl1(c1)"
    mock_engine.ssert_called_with(sql)


def test_db_models_utils_create_index_can_not_delete(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.execute_sql_cmd', mock_engine)
    mocker.patch('src.db_models.utils.check_index_exists', Mock(return_value=True))

    create_index(table_name='tbl1', idx='idx', column='c1')
    mock_engine.assert_not_called()

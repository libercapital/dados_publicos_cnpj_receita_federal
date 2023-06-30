from unittest.mock import Mock

from src.db_models.utils import delete_pk


def test_db_models_utils_delete_pk_can_delete(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.execute_sql_cmd', mock_engine)
    mocker.patch('src.db_models.utils.check_pk_exists', Mock(return_value=True))

    delete_pk(table_name='tbl1', pk='pk1')
    sql = "alter table tbl1 drop constraint pk1"
    mock_engine.assert_called_with(sql)


def test_db_models_utils_delete_pk_can_not_delete(mocker):
    mock_engine = Mock()
    mocker.patch('src.db_models.utils.execute_sql_cmd', mock_engine)
    mocker.patch('src.db_models.utils.check_pk_exists', Mock(return_value=False))

    delete_pk(table_name='tbl1', pk='pk1')
    mock_engine.assert_not_called()

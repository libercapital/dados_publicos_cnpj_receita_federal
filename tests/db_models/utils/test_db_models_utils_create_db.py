from unittest import mock

from src.db_models.utils import create_db


@mock.patch('src.db_models.utils.settings.ENGINE_NO_DB.connect')
def test_db_models_utils_create_db_ok(mock_engine):
    cursor_mock = mock_engine.return_value.__enter__.return_value
    create_db()
    sql = "CREATE DATABASE rf_dados_publicos_cnpj_db_test;"
    cursor_mock.execute.assert_called_with(sql)

from unittest.mock import Mock

import pandas

from src.engine.company_root_simples import CompanyRootSimples
from .fixtures import mock_load_dicts_code_to_name

data_mock = [
    ["98760861", "N", "20070701", "20140509", "N", "00000000", "00000000"],
    ["98761000", "N", "20070701", "20090716", "N", "00000000", "00000000"],
    ["98761091", "S", "20070701", "00000000", "N", "00000000", "00000000"],
    ["98762693", "N", "20070701", "20150630", "N", "00000000", "00000000"],
    ["98762792", "N", "20070701", "20110930", "N", "00000000", "00000000"],
    ["98763352", "N", "20070701", "20161208", "N", "00000000", "00000000"],
    ["98764285", "S", "20070701", "00000000", "N", "00000000", "00000000"],
    ["98764665", "S", "20070701", "00000000", "N", "00000000", "00000000"],
    ["98819295", "S", "20070701", "00000000", "N", "00000000", "00000000"],
    ["98819568", "N", "20070701", "20071126", "S", "20070701", "20071126"],
]

columns_csv = ['cnpj_root', 'simples_option_code', 'simples_entry_date', 'simples_exit_date',
               'mei_option_code', 'mei_entry_date', "mei_exit_date"]


def test_engine_company_root_simples_parse_file(mocker):
    mock_engine = Mock()
    mock_df_to_database = Mock()
    mock_get_list_files = Mock()

    def mock_data(sep, encoding, header, dtype, engine, memory_map, filepath_or_buffer, names, chunksize):
        return [pandas.DataFrame(data=data_mock, columns=columns_csv)]

    mocker.patch('src.engine.company_root_simples.CompanyRootSimples.load_dicts_code_to_name',
                 mock_load_dicts_code_to_name)
    mocker.patch('src.engine.company_root_simples.CompanyRootSimples.get_list_files', mock_get_list_files)
    mocker.patch('src.engine.company_root_simples.settings.ENGINE', mock_engine)
    mocker.patch('src.engine.company_root_simples.df_to_database', mock_df_to_database)
    mocker.patch('src.engine.company_root_simples.pd.read_csv', mock_data)

    data_expected = [
        ["98760861", "N", "2007-07-01", "2014-05-09", "N", "", "", "NÃO", "NÃO"],
        ["98761000", "N", "2007-07-01", "2009-07-16", "N", "", "", "NÃO", "NÃO"],
        ["98761091", "S", "2007-07-01", "", "N", "", "", "SIM", "NÃO"],
        ["98762693", "N", "2007-07-01", "2015-06-30", "N", "", "", "NÃO", "NÃO"],
        ["98762792", "N", "2007-07-01", "2011-09-30", "N", "", "", "NÃO", "NÃO"],
        ["98763352", "N", "2007-07-01", "2016-12-08", "N", "", "", "NÃO", "NÃO"],
        ["98764285", "S", "2007-07-01", "", "N", "", "", "SIM", "NÃO"],
        ["98764665", "S", "2007-07-01", "", "N", "", "", "SIM", "NÃO"],
        ["98819295", "S", "2007-07-01", "", "N", "", "", "SIM", "NÃO"],
        ["98819568", "N", "2007-07-01", "2007-11-26", "S", "2007-07-01", "2007-11-26", "NÃO", "SIM"],
    ]

    df_expected = pandas.DataFrame(data=data_expected,
                                   columns=columns_csv + ["simples_option_desc", "mei_option_desc"])

    CompanyRootSimples().parse_file(file='dir/test.csv')

    mock_df_to_database.assert_called()
    df_parsed = mock_df_to_database.call_args[1]['df']

    pandas.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=None)

from unittest.mock import Mock

import pandas

from src.engine.partners import Partners
from .fixtures import mock_load_dicts_code_to_name

data_mock = [
    ["38424667", "2", "DAIANE", "***123456**", "49", "20200911", None, "***000000**", None, "00", "4"],
    ["38424722", "2", "EDNAILTON", "***123456**", "49", "20200911", None, "***000000**", None, "00", "4"],
    ["38424742", "2", "HOMERO", "***123456**", "65", "20200813", None, "***000000**", None, "00", "7"],
    ["38424786", "2", "LUCIANA", "***123456**", "49", "20200911", None, "***000000**", None, "00", "6"],
    ["34717866", "2", "EDER", "***123456**", "22", "20190830", None, "***000000**", None, "00", "4"],
    ["34717866", "2", "AGNALDO", "***123456**", "49", "20190830", None, "***000000**", None, "00",
     "4"],
    ["34717866", "2", "THATIELY", "***123456**", "22", "20190830", None, "***000000**", None,
     "00", "5"],
    ["38424860", "2", "DIONE", "***123456**", "49", "20200909", None, "***000000**", None, "00",
     "4"],
    ["38424860", "2", "SILASNE", "***123456**", "49", "20200909", None, "***000000**", None, "00", "5"],
    ["38424994", "2", "SIL", "***123456**", "49", "20200911", None, "***000000**", None, "00", "4"],
]

columns_csv = ['cnpj_root', 'type_partner_code', 'name', 'partner_doc', 'qualification_code', 'entry_date', "country",
               "legal_representation_name", "legal_representation_doc", "legal_representation_qualification_code",
               "age_band_code"]


def test_engine_partners_parse_file(mocker):
    mock_engine = Mock()
    mock_df_to_database = Mock()
    mock_get_list_files = Mock()

    def mock_data(sep, encoding, header, dtype, engine, memory_map, filepath_or_buffer, names, chunksize):
        return [pandas.DataFrame(data=data_mock, columns=columns_csv)]

    mocker.patch('src.engine.partners.Partners.load_dicts_code_to_name',
                 mock_load_dicts_code_to_name)
    mocker.patch('src.engine.partners.Partners.get_list_files', mock_get_list_files)
    mocker.patch('src.engine.partners.settings.ENGINE', mock_engine)
    mocker.patch('src.engine.partners.df_to_database', mock_df_to_database)
    mocker.patch('src.engine.partners.pd.read_csv', mock_data)

    data_expected = [
        ["38424667", "2", "DAIANE", "***123456**", "49", "2020-09-11", None, "***000000**", None, "00", "4",
         "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "31 a 40 ANOS"],
        ["38424722", "2", "EDNAILTON", "***123456**", "49", "2020-09-11", None, "***000000**", None, "00",
         "4", "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "31 a 40 ANOS"],
        ["38424742", "2", "HOMERO", "***123456**", "65", "2020-08-13", None, "***000000**", None, "00", "7",
         "PESSOA FÍSICA", "TITULAR PESSOA FÍSICA RESIDENTE OU DOMICILIADO NO BRASIL", "NÃO INFORMADA", "61 a 70 ANOS"],
        ["38424786", "2", "LUCIANA", "***123456**", "49", "2020-09-11", None, "***000000**", None, "00",
         "6", "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "51 a 60 ANOS"],
        ["34717866", "2", "EDER", "***123456**", "22", "2019-08-30", None, "***000000**", None, "00",
         "4", "PESSOA FÍSICA", "SÓCIO", "NÃO INFORMADA", "31 a 40 ANOS"],
        ["34717866", "2", "AGNALDO", "***123456**", "49", "2019-08-30", None, "***000000**", None,
         "00", "4", "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "31 a 40 ANOS"],
        ["34717866", "2", "THATIELY", "***123456**", "22", "2019-08-30", None, "***000000**",
         None, "00", "5", "PESSOA FÍSICA", "SÓCIO", "NÃO INFORMADA", "41 a 50 ANOS"],
        ["38424860", "2", "DIONE", "***123456**", "49", "2020-09-09", None, "***000000**", None,
         "00", "4", "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "31 a 40 ANOS"],
        ["38424860", "2", "SILASNE", "***123456**", "49", "2020-09-09", None, "***000000**", None, "00", "5",
         "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "41 a 50 ANOS"],
        ["38424994", "2", "SIL", "***123456**", "49", "2020-09-11", None, "***000000**", None, "00", "4",
         "PESSOA FÍSICA", "SÓCIO-ADMINISTRADOR", "NÃO INFORMADA", "31 a 40 ANOS"]
    ]

    df_expected = pandas.DataFrame(data=data_expected,
                                   columns=columns_csv + ["type_partner_desc", "qualification_desc",
                                                          "legal_representation_qualification_desc", "age_band_desc"])

    Partners().parse_file(file='dir/test.csv')

    mock_df_to_database.assert_called()
    df_parsed = mock_df_to_database.call_args[1]['df']

    pandas.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=None)

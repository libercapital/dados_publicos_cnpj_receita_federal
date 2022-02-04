from unittest.mock import Mock

import pandas

from src.engine.company_root import CompanyRoot
from .fixtures import mock_load_dicts_code_to_name

data_mock = [
    ["98819303", "JUREMA ALBINO DE LIMA", "2135", "50", "0,00", "02", ""],
    ["98819402", "EMPRESA DINDINHO DE TRANSPORTES LTDA", "2062", "49", "0,00", "03", ""],
    ["98819410", "LEONILDA ROST DE BORBA", "2135", "50", "0,00", "05", ""],
    ["98819519", "IMOBILIARIA LITORANEA LTDA", "2062", "49", "0,00", "05", ""],
    ["98819543", "NATALINA MESSAGIO DIAS", "2135", "50", "0,00", "05", ""],
    ["98819550", "ANTONIO ORIQUES CARDOSO", "2135", "50", "0,00", "01", ""],
    ["98819568", "ELI ORIQUES CARDOSO", "2046", "50", "0,00", "01", ""],
    ["98819600", "PAULINO LEMOS DA SILVA", "2135", "50", "0,00", "05", ""],
    ["98819832", "JOAO FELTRIN", "2135", "8", "0,00", "01", ""],
    ["99017782", "SOCIEDADE UNIAO DE ARTISTAS", "3999", "16", "5231,12", "05", ""],
]

columns_csv = ['cnpj_root', 'name', 'legal_nature_code', 'liable_qualification_code',
               'social_capital', 'size_code', "efr"]


def test_engine_company_root_parse_file(mocker):
    mock_engine = Mock()
    mock_df_to_database = Mock()
    mock_get_list_files = Mock()

    def mock_data(sep, encoding, header, dtype, engine, memory_map, filepath_or_buffer, names, chunksize):
        return [pandas.DataFrame(data=data_mock, columns=columns_csv)]

    mocker.patch('src.engine.company_root.CompanyRoot.load_dicts_code_to_name', mock_load_dicts_code_to_name)
    mocker.patch('src.engine.company_root.CompanyRoot.get_list_files', mock_get_list_files)
    mocker.patch('src.engine.company_root.settings.ENGINE', mock_engine)
    mocker.patch('src.engine.company_root.df_to_database', mock_df_to_database)
    mocker.patch('src.engine.company_root.pd.read_csv', mock_data)

    data_expected = [
        ["98819303", "JUREMA ALBINO DE LIMA", "2135", "50", 0.0, "02", "", "EMPRESÁRIO (INDIVIDUAL)", "EMPRESÁRIO",
         "MICRO EMPRESA"],
        ["98819402", "EMPRESA DINDINHO DE TRANSPORTES LTDA", "2062", "49", 0.0, "03", "",
         "SOCIEDADE EMPRESÁRIA LIMITADA",
         "SÓCIO-ADMINISTRADOR", "EMPRESA DE PEQUENO PORTE"],
        ["98819410", "LEONILDA ROST DE BORBA", "2135", "50", 0.0, "05", "", "EMPRESÁRIO (INDIVIDUAL)", "EMPRESÁRIO",
         "DEMAIS"],
        ["98819519", "IMOBILIARIA LITORANEA LTDA", "2062", "49", 0.0, "05", "", "SOCIEDADE EMPRESÁRIA LIMITADA",
         "SÓCIO-ADMINISTRADOR", "DEMAIS"],
        ["98819543", "NATALINA MESSAGIO DIAS", "2135", "50", 0.0, "05", "", "EMPRESÁRIO (INDIVIDUAL)", "EMPRESÁRIO",
         "DEMAIS"],
        ["98819550", "ANTONIO ORIQUES CARDOSO", "2135", "50", 0.0, "01", "", "EMPRESÁRIO (INDIVIDUAL)", "EMPRESÁRIO",
         "NÃO INFORMADO"],
        ["98819568", "ELI ORIQUES CARDOSO", "2046", "50", 0.0, "01", "", "SOCIEDADE ANÔNIMA ABERTA", "EMPRESÁRIO",
         "NÃO INFORMADO"],
        ["98819600", "PAULINO LEMOS DA SILVA", "2135", "50", 0.0, "05", "", "EMPRESÁRIO (INDIVIDUAL)", "EMPRESÁRIO",
         "DEMAIS"],
        ["98819832", "JOAO FELTRIN", "2135", "8", 0.0, "01", "", "EMPRESÁRIO (INDIVIDUAL)",
         "CONSELHEIRO DE ADMINISTRAÇÃO",
         "NÃO INFORMADO"],
        ["99017782", "SOCIEDADE UNIAO DE ARTISTAS", "3999", "16", 5231.12, "05", "", "ASSOCIAÇÃO PRIVADA", "PRESIDENTE",
         "DEMAIS"]

    ]

    df_expected = pandas.DataFrame(data=data_expected,
                                   columns=columns_csv + ["legal_nature_desc", "liable_qualification_desc",
                                                          "size_desc"])

    CompanyRoot().parse_file(file='dir/test.csv')

    mock_df_to_database.assert_called()
    df_parsed = mock_df_to_database.call_args[1]['df']
    pandas.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=None)

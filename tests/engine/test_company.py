from unittest.mock import Mock

import pandas

from src.engine.company import Company
from .fixtures import mock_load_dicts_code_to_name

data_mock = [
    ["30459277", "0001", "48", "1", "VR CARVOARIA", "02", "20180515", "00", "", "", "20180515", "0210108",
     "0151201,0151202,0220902,0230600,4671100,4681803,4789099,4930201,4930202", "FAZENDA", "TRONCO", "SN", "",
     "ZONA RURAL", "123456789", "MG", "0574", "38", "123456789", "38", "123456789", "38", "123456789",
     "email1@gmail.com", "", ""],
    ["30459293", "0001", "30", "1", "", "04", "20210317", "63", "", "", "20180515", "1091101", "", "RUA",
     "JOSE TOMACHESKI", "451", "", "GUARAITUBA", "83406150", "PR", "7513", "41", "99999999", "", "", "", "", "", "",
     ""],
    ["30459303", "0001", "38", "1", "MERCADINHO LEMOS", "02", "20180515", "00", "", "", "20180515", "4712100", "",
     "RUA", "NOSSA SENHORA APARECIDA", "532", "", "JARDIM BANDEIRANTES", "61934200", "CE", "1585", "85", "123456789",
     "", "", "", "", "", "", ""],
    ["30459318", "0001", "04", "1", "CORACAO AMARELO", "08", "20181114", "01", "", "", "20180515", "8599699",
     "4761001,5811500,5819100,5813100", "RUA", "15 DE NOVEMBRO", "403", "", "CENTRO", "123456789", "RS", "8729",
     "51", "123456789", "", "", "", "", "email2@gmail.com", "", ""],
    ["30459329", "0001", "86", "1", "MDLP PRESTADORA DE SERVICOS", "02", "20180515", "00", "", "", "20180515",
     "4744099", "", "RUA", "ANDRE ROCHA", "4600", "CASA 04 B FUNDOS", "TAQUARA", "22710561", "RJ", "6001", "21",
     "123456789", "", "", "", "", "email3@gmail.com", "", ""],
    ["30459342", "0001", "35", "1", "CIDA", "02", "20180515", "00", "", "", "20180515", "8712300", "", "RUA",
     "CAMILO CASTELO BRANCO", "121", "CASA 1", "JARDIM ELVIRA", "06243070", "SP", "6789", "11", "123456789", "", "",
     "", "", "email31@gmail.com", "", ""],
    ["30459353", "0001", "15", "1", "RODRIGO VENZI FERREIRA", "02", "20180515", "00", "", "", "20180515", "9529106",
     "", "RUA", "JOSE GREGORIO DE GUZZI", "700", "", "PARQUE RESIDENCIAL JOAO DA SILVA", "123456789", "SP", "7097",
     "17", "123456789", "", "", "", "", "email4@gmail.com", "", ""],
    ["30459363", "0001", "50", "1", "W.M.CALDEIRARIA E MANUTENCAO DE IMPLEMENTOS AGRICOLAS", "04", "20210310", "63",
     "", "", "20180515", "3314711", "4330404,2539001,3314712,4520001", "RUA", "FRANCISCO FURTUOSO EVANGELISTA",
     "1395", "", "CDHU", "19275000", "SP", "7255", "18", "123456789", "", "", "", "", "", "", ""],
    ["30459373", "0001", "96", "1", "HORTIFRUTA IDEAL", "02", "20180515", "00", "", "", "20180515", "4724500", "",
     "RUA", "JOAO DAYREL FILHO", "125", "", "IUNA", "38616570", "MG", "5407", "38", "123456789", "", "", "", "", "",
     "", ""],
    ["30459386", "0001", "65", "1", "PERFORMANCE LAVACAR E ESTETICA AUTOMOTIVA", "02", "20180515", "00", "", "",
     "20180515", "4520005", "", "AVENIDA", "GETULIO VARGAS", "1034", "", "CENTRO", "86455000", "PR", "7649", "43",
     "99688261", "", "", "", "", "", "", ""],
    ["30459398", "0001", "90", "1", "LOJA DONA BELLA", "08", "20190401", "01", "", "", "20180515", "4781400",
     "4783102,4789099,4782201", "RUA", "FONTANA DEL TRITONE (GRAN PARQUE HELIO MIRANDA)", "406", "",
     "JARDIM PLANALTO", "123456789", "SP", "6831", "19", "123456789", "", "", "", "", "email5@gmail.com", "", ""],
]

columns_csv = ['cnpj_root', 'cnpj_branch', 'cnpj_digit', 'headquarters', 'trade_name', 'situation_code',
               'situation_date', 'situation_reason_code', 'city_outer_name', 'country_outer_name',
               'foundation_date', 'cnae_main', 'cnae_sec', 'address_type', 'address', 'address_number',
               'address_complement', 'address_neighborhood', 'address_zip_code', 'address_fu',
               'address_city_code', 'tel1_dd', 'tel1', 'tel2_dd', 'tel2', 'fax_dd', 'fax', 'email',
               'special_situation', 'special_situation_date']


def test_engine_company_parse_file(mocker):
    mock_engine = Mock()
    mock_df_to_database = Mock()
    mock_get_list_files = Mock()

    def mock_data(sep, encoding, header, dtype, engine, memory_map, filepath_or_buffer, names, chunksize):
        return [pandas.DataFrame(data=data_mock, columns=columns_csv)]

    mocker.patch('src.engine.company.Company.load_dicts_code_to_name', mock_load_dicts_code_to_name)
    mocker.patch('src.engine.company.Company.get_list_files', mock_get_list_files)
    mocker.patch('src.engine.company.settings.ENGINE', mock_engine)
    mocker.patch('src.engine.company.df_to_database', mock_df_to_database)
    mocker.patch('src.engine.company.pd.read_csv', mock_data)

    data_expected = [
        ["30459277", "0001", "48", True, "VR CARVOARIA", "02", "2018-05-15", "00", "", "", "2018-05-15", "0210108",
         "0151201,0151202,0220902,0230600,4671100,4681803,4789099,4930201,4930202", "FAZENDA", "TRONCO",
         "SN", "", "ZONA RURAL", "123456789", "MG", "0574", "38", "123456789", "38", "123456789", "38", "123456789",
         "email1@gmail.com", "", "", "30459277000148", "ATIVA", "SEM MOTIVO"],
        ["30459293", "0001", "30", True, "", "04", "2021-03-17", "63", "", "", "2018-05-15", "1091101", "", "RUA",
         "JOSE TOMACHESKI", "451", "", "GUARAITUBA", "83406150", "PR", "7513", "41", "99999999", "", "", "", "", "", "",
         "", "30459293000130", "INAPTA", "OMISSAO DE DECLARACOES", "COLOMBO"],
        ["30459303", "0001", "38", True, "MERCADINHO LEMOS", "02", "2018-05-15", "00", "", "", "2018-05-15",
         "4712100", "", "RUA", "NOSSA SENHORA APARECIDA", "532", "", "JARDIM BANDEIRANTES", "61934200", "CE", "1585",
         "85", "123456789", "", "", "", "", "", "", "", "30459303000138", "ATIVA", "SEM MOTIVO", "MARACANAU"],
        ["30459318", "0001", "04", True, "CORACAO AMARELO", "08", "2018-11-14", "01", "", "", "2018-05-15", "8599699",
         "4761001,5811500,5819100,5813100", "RUA", "15 DE NOVEMBRO", "403", "", "CENTRO", "123456789", "RS",
         "8729", "51", "123456789", "", "", "", "", "email2@gmail.com", "", "", "30459318000104", "BAIXADA",
         "EXTINCAO POR ENCERRAMENTO LIQUIDACAO VOLUNTARIA", "LAJEADO"],
        ["30459329", "0001", "86", True, "MDLP PRESTADORA DE SERVICOS", "02", "2018-05-15", "00", "", "",
         "2018-05-15", "4744099", "", "RUA", "ANDRE ROCHA", "4600", "CASA 04 B FUNDOS", "TAQUARA", "22710561", "RJ",
         "6001", "21", "123456789", "", "", "", "", "email3@gmail.com", "", "", "30459329000186", "ATIVA",
         "SEM MOTIVO", "RIO DE JANEIRO"],
        ["30459342", "0001", "35", True, "CIDA", "02", "2018-05-15", "00", "", "", "2018-05-15", "8712300", "", "RUA",
         "CAMILO CASTELO BRANCO", "121", "CASA 1", "JARDIM ELVIRA", "06243070", "SP", "6789", "11", "123456789", "", "",
         "", "", "email31@gmail.com", "", "", "30459342000135", "ATIVA", "SEM MOTIVO", "OSASCO"],
        ["30459353", "0001", "15", True, "RODRIGO VENZI FERREIRA", "02", "2018-05-15", "00", "", "", "2018-05-15",
         "9529106", "", "RUA", "JOSE GREGORIO DE GUZZI", "700", "", "PARQUE RESIDENCIAL JOAO DA SILVA", "123456789",
         "SP", "7097", "17", "123456789", "", "", "", "", "email4@gmail.com", "", "", "30459353000115", "ATIVA",
         "SEM MOTIVO", "SAO JOSE DO RIO PRETO"],
        ["30459363", "0001", "50", True, "W.M.CALDEIRARIA E MANUTENCAO DE IMPLEMENTOS AGRICOLAS", "04", "2021-03-10",
         "63", "", "", "2018-05-15", "3314711", "4330404,2539001,3314712,4520001", "RUA",
         "FRANCISCO FURTUOSO EVANGELISTA", "1395", "", "CDHU", "19275000", "SP", "7255", "18", "123456789", "", "", "",
         "", "", "", "", "30459363000150", "INAPTA", "OMISSAO DE DECLARACOES", "EUCLIDES DA CUNHA PAULISTA"],
        ["30459373", "0001", "96", True, "HORTIFRUTA IDEAL", "02", "2018-05-15", "00", "", "", "2018-05-15",
         "4724500", "", "RUA", "JOAO DAYREL FILHO", "125", "", "IUNA", "38616570", "MG", "5407", "38", "123456789", "",
         "", "", "", "", "", "", "30459373000196", "ATIVA", "SEM MOTIVO", "UNAI"],
        ["30459386", "0001", "65", True, "PERFORMANCE LAVACAR E ESTETICA AUTOMOTIVA", "02", "2018-05-15", "00", "",
         "", "2018-05-15", "4520005", "", "AVENIDA", "GETULIO VARGAS", "1034", "", "CENTRO", "86455000", "PR", "7649",
         "43", "99688261", "", "", "", "", "", "", "", "30459386000165", "ATIVA", "SEM MOTIVO", "JOAQUIM TAVORA"],
        ["30459398", "0001", "90", True, "LOJA DONA BELLA", "08", "2019-04-01", "01", "", "", "2018-05-15", "4781400",
         "4783102,4789099,4782201", "RUA", "FONTANA DEL TRITONE (GRAN PARQUE HELIO MIRANDA)", "406", "",
         "JARDIM PLANALTO", "123456789", "SP", "6831", "19", "123456789", "", "", "", "", "email5@gmail.com", "", "",
         "30459398000190", "BAIXADA", "EXTINCAO POR ENCERRAMENTO LIQUIDACAO VOLUNTARIA", "PAULINIA"],
    ]

    df_expected = pandas.DataFrame(data=data_expected,
                                   columns=columns_csv + ['cnpj', 'situation_desc', 'situation_reason_desc',
                                                          'address_city_name'])

    Company().parse_file(file='dir/test.csv')

    mock_df_to_database.assert_called()
    df_parsed = mock_df_to_database.call_args[1]['df']

    df_expected['special_situation_date'] = pandas.to_datetime(df_expected['special_situation_date'])
    df_parsed['special_situation_date'] = pandas.to_datetime(df_parsed['special_situation_date'])
    pandas.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=None)

from unittest.mock import Mock

import pandas

from src.engine.company_tax_regime import CompanyTaxRegime
from .fixtures import mock_load_dicts_code_to_name

data_mock = [
    ['2020', '00.055.699/0001-97', 'LUCRO ARBITRADO', 'GOIANIA', 'GO'],
    ['2020', '00.091.639/0001-20', 'LUCRO PRESUMIDO', 'GOIANIA', 'GO'],
    ['2020', '00.198.451/0001-85', 'LUCRO PRESUMIDO', 'JUAZEIRO DO NORTE', 'CE'],
    ['2020', '00.287.036/0001-06', 'LUCRO REAL', 'VERANOPOLIS', 'RS'],
    ['2020', '00.360.051/0001-24', 'LUCRO ARBITRADO', 'EMBU DAS ARTES', 'SP'],
    ['2020', '00.393.163/0001-81', 'IMUNE DO IRPJ', 'FORTALEZA', 'CE'],
    ['2020', '00.429.957/0001-58', 'LUCRO ARBITRADO', 'UMUARAMA', 'PR'],
    ['2020', '00.441.228/0001-17', 'IMUNE DO IRPJ', 'FORTALEZA', 'CE'],
]

columns_csv = ['ref_year', 'cnpj', 'tax_regime', 'city_name', 'fu']


def test_engine_company_tax_regime_parse_file(mocker):
    mock_engine = Mock()
    mock_df_to_database = Mock()
    mock_get_list_files = Mock()

    def mock_data(sep, encoding, header, dtype, engine, memory_map, filepath_or_buffer, names, chunksize):
        return [pandas.DataFrame(data=data_mock, columns=columns_csv)]

    mocker.patch('src.engine.company_tax_regime.CompanyTaxRegime.load_dicts_code_to_name', mock_load_dicts_code_to_name)
    mocker.patch('src.engine.company_tax_regime.CompanyTaxRegime.get_list_files', mock_get_list_files)
    mocker.patch('src.engine.company_tax_regime.settings.ENGINE', mock_engine)
    mocker.patch('src.engine.company_tax_regime.df_to_database', mock_df_to_database)
    mocker.patch('src.engine.company_tax_regime.pd.read_csv', mock_data)

    data_expected = [
        ['2020', '00055699000197', 'LUCRO ARBITRADO', 'GOIANIA', 'GO', '00055699'],
        ['2020', '00091639000120', 'LUCRO PRESUMIDO', 'GOIANIA', 'GO', '00091639'],
        ['2020', '00198451000185', 'LUCRO PRESUMIDO', 'JUAZEIRO DO NORTE', 'CE', '00198451'],
        ['2020', '00287036000106', 'LUCRO REAL', 'VERANOPOLIS', 'RS', '00287036'],
        ['2020', '00360051000124', 'LUCRO ARBITRADO', 'EMBU DAS ARTES', 'SP', '00360051'],
        ['2020', '00393163000181', 'IMUNE DO IRPJ', 'FORTALEZA', 'CE', '00393163'],
        ['2020', '00429957000158', 'LUCRO ARBITRADO', 'UMUARAMA', 'PR', '00429957'],
        ['2020', '00441228000117', 'IMUNE DO IRPJ', 'FORTALEZA', 'CE', '00441228'],
    ]

    df_expected = pandas.DataFrame(data=data_expected, columns=columns_csv + ["cnpj_root"])

    CompanyTaxRegime().parse_file(file='dir/test.csv')

    mock_df_to_database.assert_called()
    df_parsed = mock_df_to_database.call_args[1]['df']
    pandas.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=None)

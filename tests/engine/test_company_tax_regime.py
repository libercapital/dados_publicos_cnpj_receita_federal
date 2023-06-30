from unittest.mock import Mock

import pandas

from src.engine.company_tax_regime import CompanyTaxRegime
from .fixtures import mock_load_dicts_code_to_name

# ref_year = Column('ref_year', String, primary_key=True)
# cnpj = Column('cnpj', String, primary_key=True, index=True)
# cnpj_scp = Column('cnpj_scp', String)
# tax_regime = Column('tax_regime', String, primary_key=True)
# amount_of_bookkeeping = Column('amount_of_bookkeeping', Float)

data_mock = [
    ['2020', '00.055.699/0001-97', '0', 'LUCRO ARBITRADO', 1],
    ['2020', '00.091.639/0001-20', '0', 'LUCRO PRESUMIDO', 1],
    ['2020', '00.198.451/0001-85', '0', 'LUCRO PRESUMIDO', 1],
    ['2020', '00.287.036/0001-06', '0', 'LUCRO REAL', 1],
    ['2020', '00.360.051/0001-24', '0', 'LUCRO ARBITRADO', 1],
    ['2020', '00.393.163/0001-81', '0', 'IMUNE DO IRPJ', 0],
    ['2020', '00.429.957/0001-58', '0', 'LUCRO ARBITRADO', 0],
    ['2020', '00.441.228/0001-17', None, 'IMUNE DO IRPJ', 0],
]

columns_csv = ['ref_year', 'cnpj', 'cnpj_scp', 'tax_regime', 'amount_of_bookkeeping']


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
        ['2020', '00055699000197', '0', 'LUCRO ARBITRADO', 1, '00055699'],
        ['2020', '00091639000120', '0', 'LUCRO PRESUMIDO', 1, '00091639'],
        ['2020', '00198451000185', '0', 'LUCRO PRESUMIDO', 1, '00198451'],
        ['2020', '00287036000106', '0', 'LUCRO REAL', 1, '00287036'],
        ['2020', '00360051000124', '0', 'LUCRO ARBITRADO', 1, '00360051'],
        ['2020', '00393163000181', '0', 'IMUNE DO IRPJ', 0, '00393163'],
        ['2020', '00429957000158', '0', 'LUCRO ARBITRADO', 0, '00429957'],
        ['2020', '00441228000117', None, 'IMUNE DO IRPJ', 0, '00441228'],
    ]

    df_expected = pandas.DataFrame(data=data_expected, columns=columns_csv + ["cnpj_root"])

    CompanyTaxRegime().parse_file(file='dir/test.csv')

    mock_df_to_database.assert_called()
    df_parsed = mock_df_to_database.call_args[1]['df']
    pandas.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=None)

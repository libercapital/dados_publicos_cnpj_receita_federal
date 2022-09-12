from unittest.mock import Mock
import os

from src.io.get_files_dict import main as get_files_dict

DIR_NAME = os.path.dirname(os.path.abspath(__file__))


class ObjectFakeText:
    def __init__(self, txt):
        self.txt = txt

    @property
    def text(self):
        return self.txt


def test_get_files_dict_keys(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    keys = ['SOCIOS', 'EMPRESAS', 'ESTABELECIMENTOS', 'TABELAS', 'TAX_REGIME', 'folder_ref_date_save_zip']

    assert sorted(dict_files.keys()) == sorted(keys)


def test_get_files_dict_keys_sub_dicts(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    tbls = ['SOCIOS', 'EMPRESAS', 'ESTABELECIMENTOS', 'TABELAS', 'TAX_REGIME']

    for tbl in tbls:
        _dict = dict_files[tbl]
        for file, dict_file in _dict.items():
            assert sorted(dict_file.keys()) == sorted(
                ['last_modified', 'file_size_bytes', 'link_to_download', 'path_save_file'])


def test_get_files_dict_empresas(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    dict_files_target = dict_files['EMPRESAS']

    assert len(dict_files_target.keys()) == 10


def test_get_files_dict_estabelecimentos(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    dict_files_target = dict_files['ESTABELECIMENTOS']

    assert len(dict_files_target.keys()) == 10


def test_get_files_dict_socios(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    dict_files_target = dict_files['SOCIOS']

    assert len(dict_files_target.keys()) == 10


def test_get_files_dict_tabelas(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    dict_files_target = dict_files['TABELAS']

    assert len(dict_files_target.keys()) == 7


def test_get_files_dict_tax_regime(fixture_get_files_dict):
    dict_files = fixture_get_files_dict
    dict_files_target = dict_files['TAX_REGIME']

    assert len(dict_files_target.keys()) == 1


def test_get_last_ref_date_mock_empresas(mocker):
    mock_requests = Mock()
    mocker.patch('src.io.get_last_ref_date.requests.get', mock_requests)
    html_file = 'test_get_last_ref_date_all_equal.html'
    html_path = os.path.join(DIR_NAME, 'htmls', html_file)
    mock_requests.return_value = ObjectFakeText(open(html_path).read())

    dict_files = get_files_dict()
    dict_files_target = dict_files['EMPRESAS']

    assert len(dict_files_target.keys()) == 10

    list_expected_files = [f'Empresas{r}.zip' for r in range(10)]

    assert sorted(dict_files_target.keys()) == sorted(list_expected_files)


def test_get_last_ref_date_mock_estabelecimentos(mocker):
    mock_requests = Mock()
    mocker.patch('src.io.get_last_ref_date.requests.get', mock_requests)
    html_file = 'test_get_last_ref_date_all_equal.html'
    html_path = os.path.join(DIR_NAME, 'htmls', html_file)
    mock_requests.return_value = ObjectFakeText(open(html_path).read())

    dict_files = get_files_dict()
    dict_files_target = dict_files['ESTABELECIMENTOS']

    assert len(dict_files_target.keys()) == 10

    list_expected_files = [f'Estabelecimentos{r}.zip' for r in range(10)]

    assert sorted(dict_files_target.keys()) == sorted(list_expected_files)


def test_get_last_ref_date_mock_socios(mocker):
    mock_requests = Mock()
    mocker.patch('src.io.get_last_ref_date.requests.get', mock_requests)
    html_file = 'test_get_last_ref_date_all_equal.html'
    html_path = os.path.join(DIR_NAME, 'htmls', html_file)
    mock_requests.return_value = ObjectFakeText(open(html_path).read())

    dict_files = get_files_dict()
    dict_files_target = dict_files['SOCIOS']

    assert len(dict_files_target.keys()) == 10

    list_expected_files = [f'Socios{r}.zip' for r in range(10)]

    assert sorted(dict_files_target.keys()) == sorted(list_expected_files)


def test_get_last_ref_date_mock_tabelas(mocker):
    mock_requests = Mock()
    mocker.patch('src.io.get_last_ref_date.requests.get', mock_requests)
    html_file = 'test_get_last_ref_date_all_equal.html'
    html_path = os.path.join(DIR_NAME, 'htmls', html_file)
    mock_requests.return_value = ObjectFakeText(open(html_path).read())

    dict_files = get_files_dict()
    dict_files_target = dict_files['TABELAS']

    assert len(dict_files_target.keys()) == 7

    list_expected_files = ['Simples.zip',
                           'Cnaes.zip',
                           'Motivos.zip',
                           'Municipios.zip',
                           'Naturezas.zip',
                           'Paises.zip',
                           'Qualificacoes.zip'
                           ]

    assert sorted(dict_files_target.keys()) == sorted(list_expected_files)

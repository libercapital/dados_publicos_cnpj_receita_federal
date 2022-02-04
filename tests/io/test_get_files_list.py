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


def test_get_files_dict_keys():
    dict_files = get_files_dict()
    keys = ['SOCIOS', 'EMPRESAS', 'ESTABELECIMENTOS', 'TABELAS', 'TAX_REGIME', 'folder_ref_date_save_zip']

    assert sorted(dict_files.keys()) == sorted(keys)


def test_get_files_dict_keys_sub_dicts():
    dict_files = get_files_dict()
    tbls = ['SOCIOS', 'EMPRESAS', 'ESTABELECIMENTOS', 'TABELAS', 'TAX_REGIME']

    for tbl in tbls:
        _dict = dict_files[tbl]
        for file, dict_file in _dict.items():
            assert sorted(dict_file.keys()) == sorted(
                ['last_modified', 'file_size_bytes', 'link_to_download', 'path_save_file'])


def test_get_files_dict_empresas():
    dict_files = get_files_dict()
    dict_files_target = dict_files['EMPRESAS']

    assert len(dict_files_target.keys()) == 10


def test_get_files_dict_estabelecimentos():
    dict_files = get_files_dict()
    dict_files_target = dict_files['ESTABELECIMENTOS']

    assert len(dict_files_target.keys()) == 10


def test_get_files_dict_socios():
    dict_files = get_files_dict()
    dict_files_target = dict_files['SOCIOS']

    assert len(dict_files_target.keys()) == 10


def test_get_files_dict_tabelas():
    dict_files = get_files_dict()
    dict_files_target = dict_files['TABELAS']

    assert len(dict_files_target.keys()) == 7


def test_get_files_dict_tax_regime():
    dict_files = get_files_dict()
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

    list_expected_files = ['K3241.K03200Y0.D10814.EMPRECSV.zip',
                           'K3241.K03200Y1.D10814.EMPRECSV.zip',
                           'K3241.K03200Y2.D10814.EMPRECSV.zip',
                           'K3241.K03200Y3.D10814.EMPRECSV.zip',
                           'K3241.K03200Y4.D10814.EMPRECSV.zip',
                           'K3241.K03200Y5.D10814.EMPRECSV.zip',
                           'K3241.K03200Y6.D10814.EMPRECSV.zip',
                           'K3241.K03200Y7.D10814.EMPRECSV.zip',
                           'K3241.K03200Y8.D10814.EMPRECSV.zip',
                           'K3241.K03200Y9.D10814.EMPRECSV.zip']

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

    list_expected_files = ['K3241.K03200Y0.D10814.ESTABELE.zip',
                           'K3241.K03200Y1.D10814.ESTABELE.zip',
                           'K3241.K03200Y2.D10814.ESTABELE.zip',
                           'K3241.K03200Y3.D10814.ESTABELE.zip',
                           'K3241.K03200Y4.D10814.ESTABELE.zip',
                           'K3241.K03200Y5.D10814.ESTABELE.zip',
                           'K3241.K03200Y6.D10814.ESTABELE.zip',
                           'K3241.K03200Y7.D10814.ESTABELE.zip',
                           'K3241.K03200Y8.D10814.ESTABELE.zip',
                           'K3241.K03200Y9.D10814.ESTABELE.zip']

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

    list_expected_files = ['K3241.K03200Y0.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y1.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y2.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y3.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y4.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y5.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y6.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y7.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y8.D10814.SOCIOCSV.zip',
                           'K3241.K03200Y9.D10814.SOCIOCSV.zip']

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

    list_expected_files = ['F.K03200$W.SIMPLES.CSV.D10814.zip',
                           'F.K03200$Z.D10814.CNAECSV.zip',
                           'F.K03200$Z.D10814.MOTICSV.zip',
                           'F.K03200$Z.D10814.MUNICCSV.zip',
                           'F.K03200$Z.D10814.NATJUCSV.zip',
                           'F.K03200$Z.D10814.PAISCSV.zip',
                           'F.K03200$Z.D10814.QUALSCSV.zip']

    assert sorted(dict_files_target.keys()) == sorted(list_expected_files)

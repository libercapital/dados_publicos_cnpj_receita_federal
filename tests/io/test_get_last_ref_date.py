import os
from unittest.mock import Mock

from src.io.get_last_ref_date import main as get_last_ref_date

core_url_expected = "https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/cadastros/consultas/dados-publicos-cnpj"
DIR_NAME = os.path.dirname(os.path.abspath(__file__))


class ObjectFakeText:
    def __init__(self, txt):
        self.txt = txt

    @property
    def text(self):
        return self.txt


def test_get_last_ref_date_all_one_date(mocker):
    mock_requests = Mock()
    mocker.patch('src.io.get_last_ref_date.requests', mock_requests)
    html_file = 'test_get_last_ref_date_all_equal.html'
    html_path = os.path.join(DIR_NAME, 'htmls', html_file)
    mock_requests.get.return_value = ObjectFakeText(open(html_path))

    ref_date = get_last_ref_date()
    ref_date_expected = '2022-08-15'

    assert ref_date == ref_date_expected


def test_get_last_ref_date_diff_dates(mocker):
    mock_requests = Mock()
    mocker.patch('src.io.get_last_ref_date.requests', mock_requests)
    html_file = 'test_get_last_ref_date_diffs.html'
    html_path = os.path.join(DIR_NAME, 'htmls', html_file)
    mock_requests.get.return_value = ObjectFakeText(open(html_path))

    ref_date = get_last_ref_date()
    ref_date_expected = '2020-01-01'

    assert ref_date == ref_date_expected

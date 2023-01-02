import json

import pandas as pd

from src.io.get_files_dict import main as get_files_dict

dict_files = get_files_dict()


def test_json_data_url_current_vs_local_cnaes():
    with open('tests/fixtures/cnaes.json', encoding='utf-8') as json_file:
        dict_expected = json.load(json_file)

    _key = None
    for key in dict_files['TABELAS']:
        if 'Cnaes' in key:
            _key = key
            break

    # get current file
    url = dict_files['TABELAS'][_key]['link_to_download']
    df = pd.read_csv(url, sep=';', encoding='cp1252', header=None)
    df[0] = df[0].astype(str)
    _dict = dict(df.values)

    # assert len dict
    assert len(_dict) == len(dict_expected), f"missing cnaes {set(_dict) - set(dict_expected)}"

    # assert same keys
    assert set(_dict.keys()) - set(dict_expected.keys()) == set()

    # assert values
    for key in _dict.keys():
        assert _dict[key] == dict_expected[key]


def test_json_data_url_current_vs_local_natju():
    with open('tests/fixtures/natju.json', encoding='utf-8') as json_file:
        dict_expected = json.load(json_file)

    _key = None
    for key in dict_files['TABELAS']:
        if 'Naturezas' in key:
            _key = key
            break

    # get current file
    url = dict_files['TABELAS'][_key]['link_to_download']
    df = pd.read_csv(url, sep=';', encoding='cp1252', header=None)
    df[0] = df[0].astype(str)
    _dict = dict(df.values)

    # assert len dict
    assert len(_dict) == len(dict_expected), f"missing natju {set(_dict) - set(dict_expected)}"

    # assert same keys
    assert set(_dict.keys()) - set(dict_expected.keys()) == set()

    # assert values
    for key in _dict.keys():
        assert _dict[key] == dict_expected[key]


def test_json_data_url_current_vs_local_qual_socio():
    with open('tests/fixtures/qual_socio.json', encoding='utf-8') as json_file:
        dict_expected = json.load(json_file)

    _key = None
    for key in dict_files['TABELAS']:
        if 'Qualificacoes' in key:
            _key = key
            break

    # get current file
    url = dict_files['TABELAS'][_key]['link_to_download']
    df = pd.read_csv(url, sep=';', encoding='cp1252', header=None)
    df[0] = df[0].astype(str)
    _dict = dict(df.values)

    # assert len dict
    assert len(_dict) == len(dict_expected), f"missing quali {set(_dict) - set(dict_expected)}"

    # assert same keys
    assert set(_dict.keys()) - set(dict_expected.keys()) == set()

    # assert values
    for key in _dict.keys():
        assert _dict[key] == dict_expected[key]


def test_json_data_url_current_vs_local_motivos():
    with open('tests/fixtures/motivos.json', encoding='utf-8') as json_file:
        dict_expected = json.load(json_file)

    _key = None
    for key in dict_files['TABELAS']:
        if 'Motivos' in key:
            _key = key
            break

    # get current file
    url = dict_files['TABELAS'][_key]['link_to_download']
    df = pd.read_csv(url, sep=';', encoding='cp1252', header=None)
    df[0] = df[0].astype(str)
    _dict = dict(df.values)

    # assert len dict
    assert len(_dict) == len(dict_expected), f"missing motivos {set(_dict) - set(dict_expected)}"

    # assert same keys
    assert set(_dict.keys()) - set(dict_expected.keys()) == set()

    # assert values
    for key in _dict.keys():
        assert _dict[key] == dict_expected[key]


def test_json_data_url_current_vs_local_pais():
    with open('tests/fixtures/pais.json', encoding='utf-8') as json_file:
        dict_expected = json.load(json_file)

    _key = None
    for key in dict_files['TABELAS']:
        if 'Paises' in key:
            _key = key
            break

    # get current file
    url = dict_files['TABELAS'][_key]['link_to_download']
    df = pd.read_csv(url, sep=';', encoding='cp1252', header=None)
    df[0] = df[0].astype(str)
    _dict = dict(df.values)

    # assert len dict
    assert len(_dict) == len(dict_expected), f"missing paises {set(_dict) - set(dict_expected)}"

    # assert same keys
    assert set(_dict.keys()) - set(dict_expected.keys()) == set()

    # assert values
    for key in _dict.keys():
        assert _dict[key] == dict_expected[key]


def test_json_data_url_current_vs_local_munic():
    with open('tests/fixtures/municipios.json', encoding='utf-8') as json_file:
        dict_expected = json.load(json_file)

    _key = None
    for key in dict_files['TABELAS']:
        if 'Municipios' in key:
            _key = key
            break

    # get current file
    url = dict_files['TABELAS'][_key]['link_to_download']
    df = pd.read_csv(url, sep=';', encoding='cp1252', header=None)
    df[0] = df[0].astype(str)
    _dict = dict(df.values)

    # assert len dict
    assert len(_dict) == len(dict_expected), f"missing municipios {set(_dict) - set(dict_expected)}"

    # assert same keys
    assert set(_dict.keys()) - set(dict_expected.keys()) == set()

    # assert values
    for key in _dict.keys():
        assert _dict[key] == dict_expected[key]

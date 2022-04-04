import json
from src.io import CNAE_JSON_NAME, NATJU_JSON_NAME, QUAL_SOCIO_JSON_NAME, MOTIVOS_JSON_NAME, PAIS_JSON_NAME, \
    MUNIC_JSON_NAME


def mock_load_dicts_code_to_name(self, file_name):
    if file_name == CNAE_JSON_NAME:
        return json.loads(open('tests/fixtures/cnaes.json', encoding='utf-8').read())
    if file_name == NATJU_JSON_NAME:
        return json.loads(open('tests/fixtures/natju.json', encoding='utf-8').read())
    if file_name == QUAL_SOCIO_JSON_NAME:
        return json.loads(open('tests/fixtures/qual_socio.json', encoding='utf-8').read())
    if file_name == MOTIVOS_JSON_NAME:
        return json.loads(open('tests/fixtures/motivos.json', encoding='utf-8').read())
    if file_name == PAIS_JSON_NAME:
        return json.loads(open('tests/fixtures/pais.json', encoding='utf-8').read())
    if file_name == MUNIC_JSON_NAME:
        return json.loads(open('tests/fixtures/municipios.json', encoding='utf-8').read())

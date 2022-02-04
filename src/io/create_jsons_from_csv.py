import json
import os

import pandas as pd

from src import DATA_FOLDER, UNZIPED_FOLDER_NAME
from src.io import CNAE_JSON_NAME, NATJU_JSON_NAME, QUAL_SOCIO_JSON_NAME, MOTIVOS_JSON_NAME, PAIS_JSON_NAME, \
    MUNIC_JSON_NAME
from src.io.get_last_ref_date import main as get_last_ref_date


def main(ref_date=None):
    ref_date = ref_date or get_last_ref_date()
    path_unziped = os.path.join(DATA_FOLDER, ref_date, UNZIPED_FOLDER_NAME)
    list_all_unziped_files = os.listdir(path_unziped)
    for file in list_all_unziped_files:
        path_file = os.path.join(path_unziped, file)
        if "CNAECSV" in file:
            _dict = create_json(path_file=path_file, path_unziped=path_unziped, json_name=CNAE_JSON_NAME)
        if "NATJUCSV" in file:
            _dict = create_json(path_file=path_file, path_unziped=path_unziped, json_name=NATJU_JSON_NAME)
        if "QUALSCSV" in file:
            _dict = create_json(path_file=path_file, path_unziped=path_unziped, json_name=QUAL_SOCIO_JSON_NAME)
        if "MOTICSV" in file:
            _dict = create_json(path_file=path_file, path_unziped=path_unziped, json_name=MOTIVOS_JSON_NAME)
        if "PAISCSV" in file:
            _dict = create_json(path_file=path_file, path_unziped=path_unziped, json_name=PAIS_JSON_NAME)
        if "MUNICCSV" in file:
            _dict = create_json(path_file=path_file, path_unziped=path_unziped, json_name=MUNIC_JSON_NAME)


def create_json(path_file, path_unziped, json_name):
    df = pd.read_csv(path_file, sep=';', encoding='cp1252', header=None)
    _dict = dict(df.values)
    path_json = os.path.join(path_unziped, json_name)
    with open(path_json, 'w', encoding='cp1252') as f:
        print(f"creating: '{path_json}'", end=' ... ', flush=True)
        json.dump(_dict, f, ensure_ascii=False)
        print('done!')
    return _dict


if __name__ == '__main__':
    main()

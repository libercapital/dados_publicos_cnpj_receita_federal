import json
import os
from abc import ABC, abstractmethod
from datetime import datetime

from src import DATA_FOLDER, UNZIPED_FOLDER_NAME
from src import settings
from src.db_models.models import dict_db_models
from src.io import CNAE_JSON_NAME, NATJU_JSON_NAME, QUAL_SOCIO_JSON_NAME, MOTIVOS_JSON_NAME, PAIS_JSON_NAME, \
    MUNIC_JSON_NAME
from src.io.get_last_ref_date import main as get_last_ref_date


class EngineCore(ABC):

    def __init__(self, type_file, table_model, n_rows_chunk=None, ref_date=None):
        self._type_file = type_file
        self._n_rows_chunk = n_rows_chunk or settings.N_ROWS_CHUNKSIZE
        self._ref_date = ref_date
        self.get_ref_date()
        self.get_all_jsons()
        self.get_list_files(type_file=type_file)

        self._tbl = table_model()
        self._table_name = self._tbl.__tablename__
        assert self._table_name in dict_db_models.keys()
        self._cols = self._tbl.list_cols()
        self._n_raw_columns = self._tbl.N_RAW_COLUMNS

        self._dict_args_read_csv = {
            'sep': ';',
            'encoding': 'latin1',
            'header': None,
            'dtype': str,
            'engine': 'c',
            'memory_map': True
        }

    def get_ref_date(self):
        """ Get ref date to get data from """
        self._ref_date = self._ref_date or get_last_ref_date()

    def __repr__(self):
        return f"{self._type_file} with ref_date: '{self._ref_date}'"

    def get_list_files(self, type_file):
        list_files_full_path = []
        if isinstance(type_file, str):
            folder_unziped = os.path.join(DATA_FOLDER, self._ref_date, UNZIPED_FOLDER_NAME)
            list_files = os.listdir(folder_unziped)
            list_files_full_path = [os.path.join(folder_unziped, file) for file in list_files if
                                    type_file in file]
        elif isinstance(type_file, list):
            folder_unziped = os.path.join(DATA_FOLDER, self._ref_date, UNZIPED_FOLDER_NAME)
            list_files = os.listdir(folder_unziped)
            for file in type_file:
                for list_file in list_files:
                    if file in list_file:
                        list_files_full_path.append(os.path.join(folder_unziped, list_file))

        self.list_files_full_path = list_files_full_path

    def load_dicts_code_to_name(self, file_name):
        full_path_file_name = os.path.join(DATA_FOLDER, self._ref_date, UNZIPED_FOLDER_NAME, file_name)
        with open(full_path_file_name, encoding='utf-8') as json_file:
            return json.load(json_file)

    def get_all_jsons(self):
        self._dict_cnae = self.load_dicts_code_to_name(file_name=CNAE_JSON_NAME)
        self._dict_natju = self.load_dicts_code_to_name(file_name=NATJU_JSON_NAME)
        self._dict_qual_socio = self.load_dicts_code_to_name(file_name=QUAL_SOCIO_JSON_NAME)
        self._dict_motivos = self.load_dicts_code_to_name(file_name=MOTIVOS_JSON_NAME)
        self._dict_pais = self.load_dicts_code_to_name(file_name=PAIS_JSON_NAME)
        self._dict_munic = self.load_dicts_code_to_name(file_name=MUNIC_JSON_NAME)

    @abstractmethod
    def delete_pk_and_indexes(self):
        pass

    @abstractmethod
    def create_pk_and_indexes(self):
        pass

    @abstractmethod
    def parse_file(self, file):
        pass

    def parse_all_files(self):
        for e, file in enumerate(sorted(self.list_files_full_path), 1):
            print(f"[{e:2}/{len(self.list_files_full_path)}] Getting file {os.path.basename(file)}")
            self.parse_file(file=file)

    @abstractmethod
    def execute(self):
        pass

    def _display_status(self, dict_status):
        total_rows_file = dict_status['total_rows_file']
        lasts_this_round = dict_status['lasts_this_round']
        lasts_since_begin_file = dict_status['lasts_since_begin_file']
        lasts_since_begin_global = dict_status['lasts_since_begin_global']
        ingestion_rate_global = self._total_rows_global / max(lasts_since_begin_global, 1)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\t\t{now:<20} | rows: {total_rows_file:<10_}/{self._total_rows_global:<10_}")
        print(
            f"\t\t{now:<20} | time: {lasts_this_round:<.2f}, since begin file {lasts_since_begin_file}, since begin global {lasts_since_begin_global} [s]")
        print(f"\t\t{now:<20} | rate: avg insert rows/s global: {ingestion_rate_global:.2f}")
        print("#" * 80)

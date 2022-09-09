import os
import time

import pandas as pd

from src import settings
from src.db_models.df_to_db import df_to_database
from src.db_models.models import Company as CompanyModel
from src.db_models.utils import delete_index, delete_pk, create_index
from src.engine.core import EngineCore
from src.io.get_last_ref_date import main as get_last_ref_date


class Company(EngineCore):
    def __init__(self, type_file='ESTABELE', table_model=CompanyModel, n_rows_chunk=None, ref_date=None):
        ref_date = ref_date or get_last_ref_date()
        super().__init__(type_file=type_file, table_model=table_model, n_rows_chunk=n_rows_chunk, ref_date=ref_date)
        self._total_rows_global = 0
        self._dict_situation_desc = {
            "01": 'NULA',
            "02": 'ATIVA',
            "03": 'SUSPENSA',
            "04": 'INAPTA',
            "08": 'BAIXADA',
        }
        self._start_time_all_files = time.time()

    def execute(self):
        self.delete_pk_and_indexes()
        self.parse_all_files()
        self.create_pk_and_indexes()

    def delete_pk_and_indexes(self):
        delete_pk(table_name=self._table_name, pk=f"{settings.DB_MODEL_COMPANY}_pkey")
        indexes_names = [f'ix_{self._table_name}_{col_index}' for col_index in self._tbl.get_index_cols()]
        for idx in indexes_names:
            delete_index(table_name=self._table_name, idx=idx)

    def create_pk_and_indexes(self):
        indexes_names = [(f'ix_{self._table_name}_{col_index}', col_index) for col_index in self._tbl.get_index_cols()]
        for idx, col_idx in indexes_names:
            create_index(table_name=self._table_name, idx=idx, column=col_idx)

    def parse_file(self, file):
        _, filename = os.path.split(file)
        dict_args_read_csv = self._dict_args_read_csv
        dict_args_read_csv['filepath_or_buffer'] = file
        dict_args_read_csv['names'] = self._cols[:self._n_raw_columns]
        dict_args_read_csv['chunksize'] = self._n_rows_chunk
        start_file = time.time()
        total_rows_file = 0
        for _df in pd.read_csv(**dict_args_read_csv):
            start_loop = time.time()
            # raw columns
            _df['cnpj_root'] = _df['cnpj_root'].astype(str).str.zfill(8)
            _df['cnpj_branch'] = _df['cnpj_branch'].astype(str).str.zfill(4)
            _df['cnpj_digit'] = _df['cnpj_digit'].astype(str).str.zfill(2)
            _df['foundation_date'] = pd.to_datetime(_df['foundation_date'], format='%Y%m%d',
                                                    errors='coerce').dt.strftime('%Y-%m-%d')
            _df['situation_date'] = pd.to_datetime(_df['situation_date'], format='%Y%m%d', errors='coerce').dt.strftime(
                '%Y-%m-%d')
            _df['special_situation_date'] = pd.to_datetime(_df['special_situation_date'], format='%Y%m%d',
                                                           errors='coerce').dt.strftime('%Y-%m-%d')
            _df['address_zip_code'] = _df['address_zip_code'].astype(str).str.replace('-', '').str.replace('\\',
                                                                                                           '').str.replace(
                '.', '').str.zfill(8)
            _df['address'] = _df['address'].str.upper()
            _df['address_neighborhood'] = _df['address_neighborhood'].str.upper()
            _df['address_complement'] = _df['address_complement'].str.upper()
            _df['address_fu'] = _df['address_fu'].str.upper()
            _df['headquarters'] = (_df['headquarters'] == '1').astype(bool)
            _df['cnae_main'] = _df['cnae_main'].str.zfill(7)
            _df['email'] = _df['email'].str.lower()
            # edited columns (not raw)
            _df['cnpj'] = _df['cnpj_root'] + _df['cnpj_branch'] + _df['cnpj_digit']
            _df['situation_desc'] = _df['situation_code'].str.zfill(2).map(self._dict_situation_desc).str.upper()
            _df['situation_reason_desc'] = _df['situation_reason_code'].astype(int).astype(str).map(
                self._dict_motivos).str.upper()
            _df['address_city_name'] = _df['address_city_code'].astype(str).map(self._dict_munic).str.upper()

            _df = _df.reindex(columns=self._cols)
            df_to_database(engine=settings.ENGINE, df=_df, table_name=self._table_name)
            self._total_rows_global += self._n_rows_chunk
            total_rows_file += self._n_rows_chunk
            lasts_this_round = round(time.time() - start_loop, 2)
            lasts_since_begin_file = round(time.time() - start_file, 2)
            lasts_since_begin_global = round(time.time() - self._start_time_all_files, 2)
            dict_status = {
                'filename': filename,
                'total_rows_file': total_rows_file,
                'lasts_this_round': lasts_this_round,
                'lasts_since_begin_file': lasts_since_begin_file,
                'lasts_since_begin_global': lasts_since_begin_global
            }
            self._display_status(dict_status)


if __name__ == '__main__':
    Company().execute()

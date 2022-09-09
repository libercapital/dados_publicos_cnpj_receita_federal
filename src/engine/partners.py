import os
import time

import pandas as pd

from src import settings
from src.db_models.df_to_db import df_to_database
from src.db_models.models import Partners as PartnersModel
from src.db_models.utils import delete_index, delete_pk, create_index
from src.engine.core import EngineCore
from src.io.get_last_ref_date import main as get_last_ref_date


class Partners(EngineCore):
    def __init__(self, type_file='SOCIOCSV', table_model=PartnersModel, n_rows_chunk=None,
                 ref_date=None):
        ref_date = ref_date or get_last_ref_date()
        super().__init__(type_file=type_file, table_model=table_model, n_rows_chunk=n_rows_chunk, ref_date=ref_date)
        self._total_rows_global = 0
        self._dict_age_band = {
            "0": 'NÃO SE APLICA',
            "1": '0 a 12 ANOS',
            "2": '13 a 20 ANOS',
            "3": "21 a 30 ANOS",
            "4": '31 a 40 ANOS',
            "5": '41 a 50 ANOS',
            "6": '51 a 60 ANOS',
            "7": '61 a 70 ANOS',
            "8": '71 a 80 ANOS',
            "9": '+80 ANOS'
        }
        self._dict_partner_code = {
            "1": "PESSOA JURÍDICA",
            "2": "PESSOA FÍSICA",
            "3": "ESTRANGEIRO",
        }
        self._start_time_all_files = time.time()

    def execute(self):
        self.delete_pk_and_indexes()
        self.parse_all_files()
        self.create_pk_and_indexes()

    def delete_pk_and_indexes(self):
        delete_pk(table_name=self._table_name, pk=f"{settings.DB_MODEL_PARTNERS}_pkey")
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
            _df['cnpj_root'] = _df['cnpj_root'].str.zfill(8)
            _df['type_partner_desc'] = _df['type_partner_code'].astype(int).astype(str).map(self._dict_partner_code)
            _df['qualification_desc'] = _df['qualification_code'].astype(int).astype(str).map(
                self._dict_qual_socio).str.upper()
            _df['legal_representation_qualification_desc'] = _df['legal_representation_qualification_code'].astype(
                int).astype(str).map(self._dict_qual_socio).str.upper()
            _df['age_band_desc'] = _df['age_band_code'].astype(int).astype(str).map(self._dict_age_band)
            _df['entry_date'] = pd.to_datetime(_df['entry_date'], format='%Y%m%d', errors='coerce').dt.strftime(
                '%Y-%m-%d')
            _df['partner_doc'] = _df['partner_doc'].fillna('-')
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
    Partners().execute()

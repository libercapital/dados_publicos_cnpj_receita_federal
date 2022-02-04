import os
import time

import pandas as pd

from src import settings
from src.db_models.df_to_db import df_to_database
from src.db_models.models import CompanyRoot as CompanyRootModel
from src.db_models.utils import delete_index, delete_pk, create_index
from src.engine.core import EngineCore
from src.io.get_last_ref_date import main as get_last_ref_date


class CompanyRoot(EngineCore):
    def __init__(self, type_file='EMPRECSV', table_model=CompanyRootModel, n_rows_chunk=100_000,
                 ref_date=get_last_ref_date()):
        super().__init__(type_file=type_file, table_model=table_model, n_rows_chunk=n_rows_chunk, ref_date=ref_date)
        self._total_rows_global = 0
        self._dict_size = {
            "01": 'NÃO INFORMADO',
            "02": "MICRO EMPRESA",
            "03": 'EMPRESA DE PEQUENO PORTE',
            "05": "DEMAIS"
        }
        self._start_time_all_files = time.time()

    def execute(self):
        self.delete_pk_and_indexes()
        self.parse_all_files()
        self.create_pk_and_indexes()

    def delete_pk_and_indexes(self):
        delete_pk(table_name=self._table_name, pk='rf_company_root_pkey')
        indexes_names = [f'ix_{self._table_name}_{col_index}' for col_index in self._tbl.get_index_cols()]
        for idx in indexes_names:
            delete_index(table_name=self._table_name, idx=idx)

    def create_pk_and_indexes(self):
        indexes_names = [(f'ix_{self._table_name}_{col_index}', col_index) for col_index in self._tbl.get_index_cols()]
        for idx, col_idx in indexes_names:
            create_index(table_name=self._table_name, idx=idx, column=col_idx)

    def parse_file(self, file):
        _, filename = os.path.split(file)
        connection = settings.ENGINE.raw_connection()
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
            _df['legal_nature_desc'] = _df['legal_nature_code'].str.zfill(4).map(self._dict_natju).str.upper()
            _df['liable_qualification_desc'] = _df['liable_qualification_code'].astype(int).astype(str).map(
                self._dict_qual_socio).str.upper()
            _df['size_desc'] = _df['size_code'].astype(str).str.zfill(2).map(self._dict_size)
            _df['social_capital'] = _df['social_capital'].astype(str).str.replace(',', '.').astype(float)

            _df = _df.reindex(columns=self._cols)
            df_to_database(connection=connection, df=_df, table_name=self._table_name)
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
    CompanyRoot().execute()

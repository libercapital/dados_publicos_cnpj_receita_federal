from sqlalchemy.types import Date, DateTime


class DBModelConfig:
    def list_cols(self):
        list_cols = [col.name for col in self.__table__.columns]
        return list_cols

    def get_pk_cols(self):
        list_cols = [col.name for col in self.__table__.columns if col.primary_key]
        return list_cols

    def get_index_cols(self):
        list_cols = [col.name for col in self.__table__.columns if col.index]
        return list_cols

    def dict_col_dtype_sqlalchemy(self):
        model_dtype = {col.name: str(col.type) for col in self.__table__.columns}
        return model_dtype

    def dict_col_dtype_pandas(self):
        model_dtype = {}
        for col in self.__table__.columns:
            _col_type = col.type.python_type
            if isinstance(col.type, (Date, DateTime)):
                _col_type = 'datetime64[ns]'

            model_dtype[col.name] = _col_type
        return model_dtype

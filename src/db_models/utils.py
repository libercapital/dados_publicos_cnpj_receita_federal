import sqlalchemy

from src import settings
from src.db_models.models import dict_db_models
from sqlalchemy import text


def execute_sql_cmd(sql):
    with settings.ENGINE.connect() as conn:
        return conn.execute(text(sql))


def check_index_exists(table_name: str, idx: str):
    sql = f"""SELECT indexname FROM pg_indexes WHERE tablename = '{table_name}'"""
    result = execute_sql_cmd(sql)
    idxs_on_table = [row[0] for row in result]
    if not idxs_on_table:
        print(f"No indexes found on: '{table_name}'")
        return False
    if idx:
        return idx in idxs_on_table


def delete_index(table_name: str, idx: str):
    msg = f"Can't delete '{idx}' on :'{table_name}' --> index does not exists"
    if check_index_exists(table_name, idx):
        sql = f"drop index {idx}"
        execute_sql_cmd(sql)
        msg = f"Delete '{idx}' from '{table_name}'"
    print(msg)


def create_index(table_name: str, idx: str, column: str):
    if check_index_exists(table_name, idx):
        print('Index already exists... exiting')
        return
    sql = f"""create index {idx} on {table_name}({column})"""
    print(f"creating index.. this can take a while.... ['{sql}'] ", flush=True)
    execute_sql_cmd(sql)
    print("Created")


def check_pk_exists(table_name: str):
    sql = f"""select * from INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE where table_name='{table_name}'"""
    result = execute_sql_cmd(sql)
    pk_on_table = [row[0] for row in result]
    if not pk_on_table:
        print(f"No pk found on: '{table_name}'")
        return False
    print(f"Found pk on: '{table_name}'")
    return True


def delete_pk(table_name: str, pk: str):
    if check_pk_exists(table_name):
        sql = f"""alter table {table_name} drop constraint {pk}"""
        print(f"dropping pk.... ['{sql}'] ", flush=True)
        execute_sql_cmd(sql)
        print("dropped")
        return
    print(f"Pk not found on: '{table_name}'")


def create_db():
    try:
        with settings.ENGINE_NO_DB.connect() as connection:
            sql = f"CREATE DATABASE {settings.POSTGRES_DB};"
            print(f"CREATING DATABASE: ['{sql}']", end='...', flush=True)
            connection.connection.set_isolation_level(0)
            connection.execute(text(sql))
            connection.connection.set_isolation_level(1)
            print('Done!')
    except sqlalchemy.exc.ProgrammingError:
        print('database already exists... skipping', end='... ')
        print('Done!')


def create_or_drop_all_tables(cmd, _dict_db_models=None):
    if not _dict_db_models:
        _dict_db_models = dict_db_models
    print(f'[{cmd.upper()} ALL TABLES]')
    for e, table_name in enumerate(_dict_db_models.keys(), 1):
        table_model = _dict_db_models[table_name]
        print(f'[{e}/{len(_dict_db_models.keys())}] {cmd} table -> {_dict_db_models[table_name].__tablename__:>30}',
              end='...', flush=True)
        _method = getattr(table_model.__table__, cmd)
        try:
            _method(bind=settings.ENGINE)
            print('Done!')
        except sqlalchemy.exc.ProgrammingError as e:
            print(f'!!! skipping with error...-> {e.args}')


def check_for_duplicated_rows(_dict_db_models=None):
    if not _dict_db_models:
        _dict_db_models = dict_db_models
    print(f'[CHECKING DATA] ALL TABLES]')
    for e, table_name in enumerate(_dict_db_models.keys(), 1):
        print(
            f'[{e}/{len(_dict_db_models.keys())}] table -> {_dict_db_models[table_name].__tablename__:>30} -- checking for data',
            end='...', flush=True)
        table_model = _dict_db_models[table_name]
        list_pks = table_model().get_pk_cols()
        pks_query = ','.join(list_pks)
        sql = f"""
        select 
            distinct {pks_query}
        from {table_name}
        group by {pks_query}
        having count(1) > 1
        """
        print(f"query\n{sql}")
        result = execute_sql_cmd(sql)
        result_fetch = result.fetchall()
        if not result_fetch:
            print(f"no duplicated row found at '{table_name}'")
            continue
        print(f"duplicated -> {table_name}")


def phoenix():
    print('[DROPPING]')
    create_or_drop_all_tables(cmd='drop', _dict_db_models=dict_db_models)
    print('[CREATING]')
    create_or_drop_all_tables(cmd='create', _dict_db_models=dict_db_models)


if __name__ == '__main__':
    check_for_duplicated_rows()

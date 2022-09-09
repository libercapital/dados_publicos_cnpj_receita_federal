import sqlalchemy

from src import settings
from src.db_models.models import dict_db_models


def check_index_exists(table_name: str, idx: str):
    sql = f"""SELECT indexname FROM pg_indexes WHERE tablename = '{table_name}'"""
    result = settings.ENGINE.execute(sql)
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
        settings.ENGINE.execute(sql)
        msg = f"Delete '{idx}' from '{table_name}'"
    print(msg)


def create_index(table_name: str, idx: str, column: str):
    if check_index_exists(table_name, idx):
        print('Index already exists... exiting')
        return
    sql = f"""create index {idx} on {table_name}({column})"""
    print(f"creating index.. this can take a while.... ['{sql}'] ", flush=True)
    settings.ENGINE.execute(sql)
    print("Created")


def check_pk_exists(table_name: str):
    sql = f"""select * from INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE where table_name='{table_name}'"""
    result = settings.ENGINE.execute(sql)
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
        settings.ENGINE.execute(sql)
        print("dropped")
        return
    print(f"Pk not found on: '{table_name}'")


def create_db():
    try:
        with settings.ENGINE_NO_DB.connect() as connection:
            sql = f"CREATE DATABASE {settings.POSTGRES_DB};"
            print(f"CREATING DATABASE: ['{sql}']", end='...', flush=True)
            connection.connection.set_isolation_level(0)
            connection.execute(sql)
            connection.connection.set_isolation_level(1)
            print('Done!')
    except sqlalchemy.exc.ProgrammingError:
        print('database already exists... skipping', end='... ')
        print('Done!')


def create_or_drop_all_tables(cmd, dict_db_models=dict_db_models):
    print(f'[{cmd.upper()} ALL TABLES]')
    for e, table_name in enumerate(dict_db_models.keys(), 1):
        table_model = dict_db_models[table_name]
        print(f'[{e}/{len(dict_db_models.keys())}] {cmd} table ->',
              dict_db_models[table_name].__tablename__,
              end='...', flush=True)
        _method = getattr(table_model.__table__, cmd)
        try:
            _method(bind=settings.ENGINE)
        except sqlalchemy.exc.ProgrammingError:
            print('skipping... ', end='... ')
        print('Done!')


def phoenix():
    print('[DROPPING]')
    create_or_drop_all_tables(cmd='drop', dict_db_models=dict_db_models)
    print('[CREATING]')
    create_or_drop_all_tables(cmd='create', dict_db_models=dict_db_models)

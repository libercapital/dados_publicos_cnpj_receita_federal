from datetime import datetime
from io import StringIO


def df_to_database(engine, df, table_name, sep='\x01', encoding='utf-8'):
    try:
        output = StringIO()
        df.to_csv(output, sep=sep, header=False, encoding=encoding, index=False)
        output.seek(0)

        # Insert data
        connection = engine.raw_connection()
        cursor = connection.cursor()
        print(f"\t\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  | sending to db", flush=True)
        cursor.copy_from(output, table_name, sep=sep, null='')
        connection.commit()
        print(f"\t\t{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  | done", flush=True)

    except Exception:

        # replace a backslash '\' somewhere in df to ''
        # sep = '\x01' issues
        # the majority of this cases does not appear often. For this reason the replace is on Exception.
        df.fillna('', inplace=True)
        string_dtypes = df.convert_dtypes().select_dtypes("string")
        df[string_dtypes.columns] = string_dtypes.applymap(lambda x: x.replace('\\', ''))

        output = StringIO()
        df.to_csv(output, sep=sep, header=False, encoding=encoding, index=False)
        output.seek(0)

        # Insert data
        connection = engine.raw_connection()
        cursor = connection.cursor()
        cursor.execute("rollback")  # rollback
        cursor.copy_from(output, table_name, sep=sep, null='')
        connection.commit()

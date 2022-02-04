import pandas as pd

from src import settings
from src.db_models.models import RefDate as RefDateModel
from src.io.get_last_ref_date import main as get_last_ref_date


def main(ref_date=None):
    ref_date = ref_date or get_last_ref_date()
    df = pd.DataFrame(columns=[RefDateModel().list_cols()[0]], data=[ref_date])
    df.to_sql(name=RefDateModel().__tablename__, con=settings.ENGINE, if_exists='replace', index=False)


if __name__ == '__main__':
    main()

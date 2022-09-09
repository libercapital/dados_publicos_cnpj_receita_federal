import os
from sqlalchemy import create_engine

N_ROWS_CHUNKSIZE = int(os.getenv('N_ROWS_CHUNKSIZE', 0)) or 100_000

POSTGRES_USER = os.getenv('POSTGRES_USER') or 'postgres'
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD') or 'postgres'
POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'postgres'
POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'rf_dados_publicos_cnpj'

db_uri_no_db = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}"
ENGINE_NO_DB = create_engine(db_uri_no_db)
db_uri = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
ENGINE = create_engine(db_uri)

DB_MODEL_COMPANY = os.getenv('DB_MODEL_COMPANY') or 'rf_company'
DB_MODEL_COMPANY_TAX_REGIME = os.getenv('DB_MODEL_COMPANY_TAX_REGIME') or 'rf_company_tax_regime'
DB_MODEL_COMPANY_ROOT = os.getenv('DB_MODEL_COMPANY_ROOT') or 'rf_company_root'
DB_MODEL_COMPANY_ROOT_SIMPLES = os.getenv('DB_MODEL_COMPANY_ROOT_SIMPLES') or 'rf_company_root_simples'
DB_MODEL_PARTNERS = os.getenv('DB_MODEL_PARTNERS') or 'rf_partners'
DB_MODEL_REF_DATE = os.getenv('DB_MODEL_REF_DATE') or 'rf_ref_date'

import os
from unittest import mock
from importlib import reload
from src import settings


def test_settings_on_env():
    """ENV values on pytest.ini"""
    from src import settings

    assert settings.N_ROWS_CHUNKSIZE == 100_000
    assert settings.POSTGRES_USER == 'postgres_user_test'
    assert settings.POSTGRES_PASSWORD == 'postgres_pw_test'
    assert settings.POSTGRES_HOST == 'postgres_host_test'
    assert settings.POSTGRES_PORT == '5432'
    assert settings.POSTGRES_DB == 'rf_dados_publicos_cnpj_db_test'

    assert settings.db_uri_no_db == "postgresql+psycopg2://postgres_user_test:postgres_pw_test@postgres_host_test:5432"
    assert settings.db_uri == "postgresql+psycopg2://postgres_user_test:postgres_pw_test@postgres_host_test:5432/rf_dados_publicos_cnpj_db_test"

    assert settings.DB_MODEL_COMPANY == 'rf_company_test'
    assert settings.DB_MODEL_COMPANY_TAX_REGIME == 'rf_company_tax_regime_test'
    assert settings.DB_MODEL_COMPANY_ROOT == 'rf_company_root_test'
    assert settings.DB_MODEL_COMPANY_ROOT_SIMPLES == 'rf_company_root_simples_test'
    assert settings.DB_MODEL_PARTNERS == 'rf_partners_test'
    assert settings.DB_MODEL_REF_DATE == 'rf_ref_date_test'


def test_settings_without_dot_env_created():
    """Not creating .env or passing without values"""

    _os_environ_test = {
        'POSTGRES_USER': '',
        'POSTGRES_PASSWORD': '',
        'POSTGRES_HOST': '',
        'POSTGRES_PORT': '',
        'POSTGRES_DB': '',
        'DB_MODEL_COMPANY': '',
        'DB_MODEL_COMPANY_TAX_REGIME': '',
        'DB_MODEL_COMPANY_ROOT': '',
        'DB_MODEL_COMPANY_ROOT_SIMPLES': '',
        'DB_MODEL_PARTNERS': '',
        'DB_MODEL_REF_DATE': '',
    }

    with mock.patch.dict(os.environ, _os_environ_test, clear=True):
        reload(settings)

        assert settings.N_ROWS_CHUNKSIZE == 100_000

        assert settings.POSTGRES_USER == 'postgres'
        assert settings.POSTGRES_PASSWORD == 'postgres'
        assert settings.POSTGRES_HOST == 'postgres'
        assert settings.POSTGRES_PORT == '5432'
        assert settings.POSTGRES_DB == 'rf_dados_publicos_cnpj'

        assert settings.db_uri_no_db == "postgresql+psycopg2://postgres:postgres@postgres:5432"
        assert settings.db_uri == "postgresql+psycopg2://postgres:postgres@postgres:5432/rf_dados_publicos_cnpj"

        assert settings.DB_MODEL_COMPANY == 'rf_company'
        assert settings.DB_MODEL_COMPANY_TAX_REGIME == 'rf_company_tax_regime'
        assert settings.DB_MODEL_COMPANY_ROOT == 'rf_company_root'
        assert settings.DB_MODEL_COMPANY_ROOT_SIMPLES == 'rf_company_root_simples'
        assert settings.DB_MODEL_PARTNERS == 'rf_partners'
        assert settings.DB_MODEL_REF_DATE == 'rf_ref_date'

    reload(settings)


def test_settings_when_env_created_custom_variables():
    """Creating a .env with not default values"""

    _os_environ_test = {
        'POSTGRES_USER': 'USER',
        'POSTGRES_PASSWORD': 'PW',
        'POSTGRES_HOST': 'HOST',
        'POSTGRES_PORT': '1234',
        'POSTGRES_DB': 'DB_NAME',
        'DB_MODEL_COMPANY': 'CMP',
        'DB_MODEL_COMPANY_TAX_REGIME': 'CMP_TX',
        'DB_MODEL_COMPANY_ROOT': 'CMP_ROOT',
        'DB_MODEL_COMPANY_ROOT_SIMPLES': 'CMP_ROOT_SMP',
        'DB_MODEL_PARTNERS': 'PART',
        'DB_MODEL_REF_DATE': 'DATE',
    }

    with mock.patch.dict(os.environ, _os_environ_test, clear=True):
        reload(settings)

        assert settings.N_ROWS_CHUNKSIZE == 100_000

        assert settings.POSTGRES_USER == 'USER'
        assert settings.POSTGRES_PASSWORD == 'PW'
        assert settings.POSTGRES_HOST == 'HOST'
        assert settings.POSTGRES_PORT == '1234'
        assert settings.POSTGRES_DB == 'DB_NAME'

        assert settings.db_uri_no_db == "postgresql+psycopg2://USER:PW@HOST:1234"
        assert settings.db_uri == "postgresql+psycopg2://USER:PW@HOST:1234/DB_NAME"

        assert settings.DB_MODEL_COMPANY == 'CMP'
        assert settings.DB_MODEL_COMPANY_TAX_REGIME == 'CMP_TX'
        assert settings.DB_MODEL_COMPANY_ROOT == 'CMP_ROOT'
        assert settings.DB_MODEL_COMPANY_ROOT_SIMPLES == 'CMP_ROOT_SMP'
        assert settings.DB_MODEL_PARTNERS == 'PART'
        assert settings.DB_MODEL_REF_DATE == 'DATE'

    reload(settings)

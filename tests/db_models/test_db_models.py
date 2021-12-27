from src.db_models.models import (dict_db_models, CompanyRoot, Company, Partners, CompanyRootSimples, CompanyTaxRegime,
                                  RefDate)


def test_db_models_models_number_of_tables():
    number_of_tables_current = len(dict_db_models.keys())
    assert number_of_tables_current == 6


def test_db_models_models_company_root():
    tbl = CompanyRoot()
    assert tbl.__tablename__ == 'rf_company_root_test'
    assert tbl.N_RAW_COLUMNS == 7
    assert sorted(tbl.get_index_cols()) == sorted(['cnpj_root'])


def test_db_models_models_company():
    tbl = Company()
    assert tbl.__tablename__ == 'rf_company_test'
    assert tbl.N_RAW_COLUMNS == 30
    assert sorted(tbl.get_index_cols()) == sorted(['cnpj', 'cnpj_root'])


def test_db_models_models_company_tax_regime():
    tbl = CompanyTaxRegime()
    assert tbl.__tablename__ == 'rf_company_tax_regime_test'
    assert tbl.N_RAW_COLUMNS == 5
    assert sorted(tbl.get_index_cols()) == sorted(['cnpj', 'cnpj_root'])


def test_db_models_models_partners():
    tbl = Partners()
    assert tbl.__tablename__ == 'rf_partners_test'
    assert tbl.N_RAW_COLUMNS == 11
    assert sorted(tbl.get_index_cols()) == sorted(['cnpj_root'])


def test_db_models_models_company_root_simples():
    tbl = CompanyRootSimples()
    assert tbl.__tablename__ == 'rf_company_root_simples_test'
    assert tbl.N_RAW_COLUMNS == 7
    assert sorted(tbl.get_index_cols()) == sorted(['cnpj_root'])


def test_db_models_models_ref_date():
    tbl = RefDate()
    assert tbl.__tablename__ == 'rf_ref_date_test'
    assert tbl.N_RAW_COLUMNS == 1
    assert sorted(tbl.get_index_cols()) == sorted(['ref_date'])

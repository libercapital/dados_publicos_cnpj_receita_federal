from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, Float, Boolean, Date
from src import settings
from src.db_models.config_models import DBModelConfig

Base = declarative_base()


class CompanyRoot(Base, DBModelConfig):
    __tablename__ = settings.DB_MODEL_COMPANY_ROOT  # empresas

    cnpj_root = Column('cnpj_root', String, primary_key=True, index=True)
    name = Column('name', String)
    legal_nature_code = Column('legal_nature_code', String)

    liable_qualification_code = Column('liable_qualification_code', String)
    social_capital = Column('social_capital', Float)
    size_code = Column('size_code', String)
    efr = Column('efr', String)

    N_RAW_COLUMNS = 7
    # RAW COLUMNS FOR PARSER ENDS HERE

    # NEW COLUMNS
    legal_nature_desc = Column('legal_nature_desc', String)
    liable_qualification_desc = Column('liable_qualification_desc', String)
    size_desc = Column('size_desc', String)


class Company(Base, DBModelConfig):
    __tablename__ = settings.DB_MODEL_COMPANY  # empresas

    cnpj_root = Column('cnpj_root', String, index=True)
    cnpj_branch = Column('cnpj_branch', String)
    cnpj_digit = Column('cnpj_digit', String)

    headquarters = Column('headquarters', Boolean)
    trade_name = Column('trade_name', String)

    situation = Column('situation_code', String)
    situation_date = Column('situation_date', Date)
    situation_reason = Column('situation_reason_code', String)

    city_outer_name = Column('city_outer_name', String)
    country_outer_name = Column('country_outer_name', String)

    foundation_date = Column('foundation_date', Date)

    cnae_main = Column('cnae_main', String)
    cnae_sec = Column('cnae_sec', String)

    # contacts
    address_type = Column('address_type', String)
    address = Column('address', String)
    address_number = Column('address_number', String)
    address_complement = Column('address_complement', String)
    address_neighborhood = Column('address_neighborhood', String)
    zip_code = Column('address_zip_code', String)
    uf = Column('address_fu', String)
    city_code = Column('address_city_code', String)
    tel1_dd = Column('tel1_dd', String)
    tel1 = Column('tel1', String)
    tel2_dd = Column('tel2_dd', String)
    tel2 = Column('tel2', String)
    fax_dd = Column('fax_dd', String)
    fax = Column('fax', String)
    email = Column('email', String)

    special_situation = Column('special_situation', String)
    special_situation_date = Column('special_situation_date', Date)

    N_RAW_COLUMNS = 30
    # RAW COLUMNS FOR PARSER ENDS HERE

    # NEW COLUMNS
    cnpj = Column('cnpj', String, primary_key=True, index=True)
    situation_desc = Column('situation_desc', String)
    situation_reason_desc = Column('situation_reason_desc', String)
    city = Column('address_city_name', String)


class Partners(Base, DBModelConfig):
    __tablename__ = settings.DB_MODEL_PARTNERS  # empresas

    cnpj_root = Column('cnpj_root', String, primary_key=True, index=True)

    type_partner_code = Column('type_partner_code', String)
    name = Column('name', String)
    partner_doc = Column('partner_doc', String, primary_key=True)
    qualification_code = Column('qualification_code', String)

    entry_date = Column('entry_date', Date)

    country = Column('country', String)

    legal_representation_name = Column('legal_representation_name', String)
    legal_representation_doc = Column('legal_representation_doc', String)
    legal_representation_qualification_code = Column('legal_representation_qualification_code', String)

    age_band_code = Column('age_band_code', String)

    N_RAW_COLUMNS = 11
    # RAW COLUMNS FOR PARSER ENDS HERE

    # NEW COLUMNS
    type_partner_desc = Column('type_partner_desc', String)
    qualification_desc = Column('qualification_desc', String)
    legal_representation_qualification_desc = Column('legal_representation_qualification_desc', String)
    age_band_desc = Column('age_band_desc', String)


class CompanyRootSimples(Base, DBModelConfig):
    __tablename__ = settings.DB_MODEL_COMPANY_ROOT_SIMPLES

    cnpj_root = Column('cnpj_root', String, primary_key=True, index=True)

    simples_option_code = Column('simples_option_code', String)
    simples_entry_date = Column('simples_entry_date', Date)
    simples_exit_date = Column('simples_exit_date', Date)

    mei_option_code = Column('mei_option_code', String)
    mei_entry_date = Column('mei_entry_date', Date)
    mei_exit_date = Column('mei_exit_date', Date)

    N_RAW_COLUMNS = 7
    # RAW COLUMNS FOR PARSER ENDS HERE

    # NEW COLUMNS
    simples_option_desc = Column('simples_option_desc', String)
    mei_option_desc = Column('mei_option_desc', String)


class CompanyTaxRegime(Base, DBModelConfig):
    __tablename__ = settings.DB_MODEL_COMPANY_TAX_REGIME

    ref_year = Column('ref_year', String)
    cnpj = Column('cnpj', String, primary_key=True, index=True)

    tax_regime = Column('tax_regime', String)
    city = Column('city_name', String)
    uf = Column('fu', String)

    N_RAW_COLUMNS = 5
    # RAW COLUMNS FOR PARSER ENDS HERE

    # NEW COLUMNS
    cnpj_root = Column('cnpj_root', String, index=True)


class RefDate(Base, DBModelConfig):
    __tablename__ = settings.DB_MODEL_REF_DATE

    ref_date = Column('ref_date', Date, primary_key=True, index=True)
    N_RAW_COLUMNS = 1


dict_db_models = {settings.DB_MODEL_COMPANY_ROOT: CompanyRoot,
                  settings.DB_MODEL_COMPANY: Company,
                  settings.DB_MODEL_COMPANY_TAX_REGIME: CompanyTaxRegime,
                  settings.DB_MODEL_PARTNERS: Partners,
                  settings.DB_MODEL_COMPANY_ROOT_SIMPLES: CompanyRootSimples,
                  settings.DB_MODEL_REF_DATE: RefDate,
                  }

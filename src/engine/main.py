from src.engine.company import Company
from src.engine.company_root import CompanyRoot
from src.engine.company_root_simples import CompanyRootSimples
from src.engine.company_tax_regime import CompanyTaxRegime
from src.engine.partners import Partners
from src.engine.ref_date import main as engine_ref_date
from src.io.get_last_ref_date import main as get_last_ref_date


def main(ref_date=None):
    ref_date = ref_date or get_last_ref_date()
    CompanyRoot(ref_date=ref_date).execute()
    Partners(ref_date=ref_date).execute()
    CompanyRootSimples(ref_date=ref_date).execute()
    CompanyTaxRegime(ref_date=ref_date).execute()
    Company(ref_date=ref_date).execute()
    engine_ref_date()


if __name__ == '__main__':
    main()

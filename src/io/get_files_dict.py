import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from src import SRC_PATH, DATA_FOLDER
from src.io import CORE_URL_FILES, HEADERS
from src.io.get_last_ref_date import main as get_last_ref_date


def main():
    """
    Get the urls from receita website
    :return: dict with urls from files as well as last modified date and size in bytes
    """
    # get last ref_date
    ref_date = get_last_ref_date()

    # get page content
    page = requests.get(CORE_URL_FILES, headers=HEADERS)

    # BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    dict_files_url = {'SOCIOS': {},
                      'EMPRESAS': {},
                      'ESTABELECIMENTOS': {},
                      'TAX_REGIME': {},
                      'TABELAS': {}}

    print('creating dict files url')
    for row in rows:
        if row.find_all('td'):
            if row.find_all('td')[1].find('a')['href'].endswith('.zip'):
                # get file_name name (ex: 'K3241.K03200Y0.D10710.SOCIOCSV.zip')
                file_name = row.find_all('td')[1].find('a')['href']
                # get last modified time and parse to date (ex: '2021-07-19')
                last_modified = datetime.strptime(row.find_all('td')[2].text.strip(), '%Y-%m-%d %H:%M').strftime(
                    '%Y-%m-%d')
                # get size file_name
                file_size = row.find_all('td')[3].text.strip()
                if 'K' in file_size:
                    file_size_bytes = float(file_size.replace('K', '')) * 2 ** 10
                elif 'M' in file_size:
                    file_size_bytes = float(file_size.replace('M', '')) * 2 ** 20
                else:
                    file_size_bytes = 0

                dict_core = {file_name: {'last_modified': last_modified,
                                         'file_size_bytes': file_size_bytes,
                                         'link_to_download': f"{CORE_URL_FILES}/{file_name}",
                                         'path_save_file': os.path.join(SRC_PATH, DATA_FOLDER, ref_date, file_name)}
                             }
                if 'Socios' in file_name:
                    dict_files_url['SOCIOS'].update(dict_core)
                elif 'Empresas' in file_name:
                    dict_files_url['EMPRESAS'].update(dict_core)
                elif 'Estabelecimentos' in file_name:
                    dict_files_url['ESTABELECIMENTOS'].update(dict_core)
                else:
                    dict_files_url['TABELAS'].update(dict_core)

    dict_files_url['folder_ref_date_save_zip'] = os.path.join(SRC_PATH, DATA_FOLDER, ref_date)

    # get page of tax regime
    _folder_tax_regime = 'regime_tributario'
    page_tax_regime = requests.get(f"{CORE_URL_FILES}/{_folder_tax_regime}", headers=HEADERS)
    soup_tax_regime = BeautifulSoup(page_tax_regime.text, 'html.parser')

    table_tax_regime = soup_tax_regime.find('table')
    rows_tax_regime = table_tax_regime.find_all('tr')
    for row in rows_tax_regime:
        if row.find_all('td'):
            if row.find_all('td')[1].find('a')['href'].endswith('.zip'):
                file_name = row.find_all('td')[1].find('a')['href']
                # get last modified time and parse to date (ex: '2021-07-19')
                last_modified = datetime.strptime(row.find_all('td')[2].text.strip(), '%Y-%m-%d %H:%M').strftime(
                    '%Y-%m-%d')
                # get size file_name
                file_size = row.find_all('td')[3].text.strip()
                if 'K' in file_size:
                    file_size_bytes = float(file_size.replace('K', '')) * 2 ** 10
                elif 'M' in file_size:
                    file_size_bytes = float(file_size.replace('M', '')) * 2 ** 20
                else:
                    file_size_bytes = 0
                dict_files_url['TAX_REGIME'].update({file_name: {'last_modified': last_modified,
                                                                 'file_size_bytes': file_size_bytes,
                                                                 'link_to_download': f"{CORE_URL_FILES}/{_folder_tax_regime}/{file_name}",
                                                                 'path_save_file': os.path.join(SRC_PATH, DATA_FOLDER,
                                                                                                ref_date, file_name)}
                                                     })

    print('Done')

    return dict_files_url


if __name__ == '__main__':
    dict_files_url = main()
    print(dict_files_url)

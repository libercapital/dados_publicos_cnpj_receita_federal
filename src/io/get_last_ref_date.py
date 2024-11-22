import requests
from bs4 import BeautifulSoup

from src.io import CORE_URL_FILES
from src.io import HEADERS


def main():
    """
    Get the urls from receita website (to see structure of dict -- see tests)
    :return: dict with urls from files as well as last modified date and size in bytes
    """
    # get page content
    _folder_open_date = 'dados_abertos_cnpj'
    page = requests.get(f'{CORE_URL_FILES}/{_folder_open_date}', headers=HEADERS)

    # BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    list_last_modified_at = []

    print('creating dict files url')
    for row in rows:
        if row.find_all('td'):
            if row.find_all('td')[1].find('a')['href'].replace('-', '').replace('/', '').isdigit():
                # get last modified time and parse to date (ex: '2021-07-19')
                list_last_modified_at.append(row.find_all('td')[1].find('a')['href'].replace('/', ''))
    # get the most common on 'last_modified' from source
    ref_date = max(list_last_modified_at)
    print('last updated date is ', ref_date)

    return ref_date


if __name__ == '__main__':
    main()
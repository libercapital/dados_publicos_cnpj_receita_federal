from collections import Counter
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

from src.io import CORE_URL_FILES, HEADERS


def main():
    """
    Get the urls from receita website (to see structure of dict -- see tests)
    :return: dict with urls from files as well as last modified date and size in bytes
    """
    # get page content
    page = requests.get(CORE_URL_FILES, headers=HEADERS)

    # BeautifulSoup object
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')
    list_last_modified_at = []

    print('creating dict files url')
    for row in rows:
        if row.find_all('td'):
            if row.find_all('td')[1].find('a')['href'].endswith('.zip'):
                # get last modified time and parse to date (ex: '2021-07-19')
                list_last_modified_at.append(
                    datetime.strptime(row.find_all('td')[2].text.strip(), '%Y-%m-%d %H:%M').strftime(
                        '%Y-%m-%d'))

    # get the most common on 'last_modified' from source
    ref_date, occurences = Counter(list_last_modified_at).most_common(1)[0]
    print(
        f"ref date will be: '{ref_date}' with {occurences} out of {len(list_last_modified_at)} ({occurences / len(list_last_modified_at):.1%}) ")
    return ref_date


if __name__ == '__main__':
    main()

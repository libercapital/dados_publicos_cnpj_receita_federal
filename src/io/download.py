import threading
import time

import requests

from src.io.get_files_dict import main as get_files_dict
from src.io.utils import create_folder, display_progress

n = 8192

dict_status = {}


def main():  # pragma: no cover
    dict_files_dict = get_files_dict()
    create_folder(dict_files_dict['folder_ref_date_save_zip'])
    started_at = time.time()
    list_threads = []
    for tbl in dict_files_dict.keys():
        _dict = dict_files_dict[tbl]
        # skip 'folder_ref_date_save_zip' key (not a dict)
        if isinstance(_dict, str):
            continue
        for file in _dict.keys():
            link_to_download = _dict[file]['link_to_download']
            path_save_file = _dict[file]['path_save_file']
            file_size_bytes = _dict[file]['file_size_bytes']
            t = threading.Thread(target=download_file,
                                 args=(file, link_to_download, path_save_file, file_size_bytes, started_at))
            t.start()
            list_threads.append(t)

    for t in list_threads:
        t.join()


def download_file(file_name, link_to_download, path_save_file, file_size_bytes, started_at):  # pragma: no cover
    """
    Download a file into local system
    :param file_name: file name
    :param link_to_download: link to download file
    :param path_save_file: path to save file
    :param file_size_bytes: size in bytes of file
    :return:
    """
    with requests.get(link_to_download, stream=True) as r:
        r.raise_for_status()
        current_file_downloaded_bytes = 0
        with open(path_save_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=n):
                f.write(chunk)
                current_file_downloaded_bytes += len(chunk)
                running_time_seconds = time.time() - started_at
                speed = current_file_downloaded_bytes / running_time_seconds if running_time_seconds > 0 else 0
                eta = (file_size_bytes - current_file_downloaded_bytes) / speed if running_time_seconds > 0 else 0
                global dict_status
                dict_status[file_name] = {'total_completed_bytes': current_file_downloaded_bytes,
                                          'file_size_bytes': file_size_bytes,
                                          'pct_downloaded': current_file_downloaded_bytes / file_size_bytes,
                                          'started_at': started_at,
                                          'running_time_seconds': running_time_seconds,
                                          'speed': speed,
                                          'eta': eta,
                                          }
                display_progress(dict_status, started_at=started_at, source='Download', th_to_display=0.001)


if __name__ == '__main__':
    main()

import os
import random
import time
from datetime import datetime
import locale

# setar locale para português
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


def create_folder(folder_path):
    """
    Create a folder given a path if not exists
    :param folder_path: path with source is 'src' folder.
            Example: folder_path='data/202008' will create a folder at $REPO/src/data/202008
    :return:
    """
    if not os.path.exists(folder_path):
        print(f"creating {folder_path}", end='... ')
        os.makedirs(folder_path)
        print('done!')


def check_if_folder_is_empty(folder_path):
    return True if len(os.listdir(folder_path)) == 0 else False


def display_progress(_dict_status, started_at, source='Download', th_to_display=0.001):  # pragma: no cover
    """
    _dict_status to print of download/unzip status (only print)
    :param _dict_status: dict with info
    :param th_to_display: threshold to display status
    :return:
    """
    total_hash = 40
    _started_at = time.time()

    if random.random() <= th_to_display:
        size_1mb_in_bytes = 1024 * 1024
        size_10mb_in_bytes = 10 * size_1mb_in_bytes
        total_bytest_completed = 0
        total_bytest_to_download = 0

        print('\r')
        print('-' * 150)
        print('#' * 30, f"NEW UPDATE [{source.upper()}]")
        print('-' * 150)
        time_since_begin = time.time() - started_at
        time_fmt = '%X'
        print(
            f"[started at]: {datetime.fromtimestamp(started_at).strftime(time_fmt)}  | [now]: {datetime.now().strftime(time_fmt)} | [lasts]: {datetime.fromtimestamp(time_since_begin).strftime(time_fmt)} \n")
        for e, _dict in enumerate(sorted(_dict_status.items())):
            _file, _dict_file = _dict
            _total_completed_bytes = _dict_file['total_completed_bytes']
            _file_size_bytes = _dict_file['file_size_bytes']
            _pct_downloaded = _dict_file['pct_downloaded']
            _eta = abs(round(_dict_file['eta'], 1))
            _speed = round(_dict_file['speed'], 3)

            total_bytest_completed += _total_completed_bytes
            total_bytest_to_download += _file_size_bytes

            size_str = 'KB'
            if _file_size_bytes >= size_10mb_in_bytes:
                _total_completed_bytes /= size_1mb_in_bytes
                _file_size_bytes /= size_1mb_in_bytes
                size_str = 'MB'

            _speed /= size_1mb_in_bytes
            step = 1 / total_hash
            _pct_downloaded = min(_pct_downloaded, 1)
            n_hash = int(_pct_downloaded / step)
            if _eta == 0 and _total_completed_bytes > 0:
                n_hash = total_hash
                _speed = 0
                _pct_downloaded = 1
                _total_completed_bytes = _file_size_bytes
            progress = '[' + '#' * n_hash + ' ' * (total_hash - n_hash) + ']'

            print(
                f"""\r{e:2}:{_file:>35} | [{(_total_completed_bytes):>5.0f}/{_file_size_bytes:>5.0f}]{size_str} ({_speed:>1.3f} {size_str}/s) | {_pct_downloaded:<3.2%} {progress} -- ETA {datetime.fromtimestamp(_eta).strftime(time_fmt)}""")

        total_pct = total_bytest_completed / total_bytest_to_download
        step = 1 / total_hash
        _pct_downloaded = min(total_pct, 1)
        n_hash = int(_pct_downloaded / step)
        total_progress = '[' + '#' * n_hash + ' ' * (total_hash - n_hash) + ']'

        total_bytest_completed /= size_1mb_in_bytes
        total_bytest_to_download /= size_1mb_in_bytes

        _total_running_time_seconds = time.time() - started_at
        _total_speed = total_bytest_completed / _total_running_time_seconds if _total_running_time_seconds > 0 else 0
        _total_eta = (
                             total_bytest_to_download - total_bytest_completed) / _total_speed if _total_running_time_seconds > 0 else 0

        print(
            f"\n\nTOTAL STATUS:  [{(total_bytest_completed):>5.0f}/{total_bytest_to_download:>5.0f}]MB | {total_pct:<3.1%} {total_progress} -- ETA {datetime.fromtimestamp(_total_eta).strftime(time_fmt)}")

        print('-' * 150)

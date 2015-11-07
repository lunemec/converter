# -*- encoding: utf-8 -*-

import argparse
import os
import platform
import shutil
import stat
import tempfile
import zipfile

from convert import ConvertedFile
from utils import text


TMP_DIR = None


def extract_binary(bin_loc):
    """
    Extracts binary from location inside .zip file to temporary directory.
    """
    package = zipfile.ZipFile(os.path.dirname(__file__), mode='r')
    global TMP_DIR
    TMP_DIR = tempfile.mkdtemp(suffix='converter')
    extracted_path = package.extract(bin_loc, TMP_DIR)
    os.chmod(extracted_path, stat.S_IXUSR)
    return extracted_path


def get_binary():
    """
    Returns path to ffmpeg binary for given operating system.
    """
    system = platform.system()
    if system == 'Linux':
        bin_loc = r'bin/ffmpeg_linux'
    elif system == 'Darwin':
        bin_loc = r'bin/ffmpeg_macos'
    elif system == 'nt':
        bin_loc = r'bin/ffmpeg_windows.exe'

    if '.zip' in __file__:
        bin_path = extract_binary(bin_loc)
    else:
        bin_path = os.path.join(os.path.dirname(__file__), bin_loc)

    return bin_path


BIN = get_binary()
VIDEO_FORMATS = ['.mkv', '.avi', '.mp4']

parser = argparse.ArgumentParser(description='Convert video files to x265.')
parser.add_argument('path', help='Root directory to start converting.')
parser.add_argument('-d', '--delete', action='store_true',
                    help='Delete original files after finishing.')


def main(args):
    dir_path = os.path.abspath(args.path)
    files_failed = []

    for root, dirs, files in os.walk(dir_path):
        for filename in sorted(files):
            filepath = os.path.abspath(os.path.join(root, filename))
            f = ConvertedFile(BIN, VIDEO_FORMATS, filepath, args.delete)
            failed = f.convert_file()

            if failed:
                files_failed.append(filepath)

    for fail in files_failed:
        text('Failed: {}'.format(fail))


def cleanup():
    """
    Removes temporary directory if present.
    """
    global TMP_DIR
    if TMP_DIR:
        try:
            shutil.rmtree(TMP_DIR)
        except IOError:
            # We probably don't have access to our own tmp directory, well
            # nothing we can do about it.
            pass


try:
    args = parser.parse_args()
    main(args)
except KeyboardInterrupt:
    text('Exiting.')
finally:
    cleanup()

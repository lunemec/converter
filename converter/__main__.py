# -*- encoding: utf-8 -*-

import argparse
import os
import shutil
import stat
import subprocess
import tempfile
import traceback
import zipfile


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
    if os.name == 'posix':  # TODO MacOS also says it is unix.
        bin_loc = r'bin/ffmpeg_unix'
    elif os.name == 'nt':
        bin_loc = r'bin/ffmpeg.exe'

    if '.zip' in __file__:
        bin_path = extract_binary(bin_loc)
    else:
        bin_path = os.path.join(os.path.dirname(__file__), bin_loc)

    return bin_path


BIN = get_binary()
VIDEO_FORMATS = ['.mkv', '.avi', '.mp4']

parser = argparse.ArgumentParser(description='Convert video files to x265.')
parser.add_argument('path', help='Root directory to start converting.')


def stamp_file(filepath, ext='stamp'):
    filename, _ = os.path.splitext(filepath)
    return '{}.{}'.format(filename, ext)


def create_start_stamp(filepath):
    """
    Creates stamp signaling we started converting given file.
    """
    stamp = stamp_file(filepath, ext='sstamp')
    with open(stamp, 'wb'):
        os.utime(stamp, None)


def create_end_stamp(filepath):
    """
    Creates stamp signaling we have successfully converted given file.
    Also removes start stamp.
    """
    start_stamp = stamp_file(filepath, ext='sstamp')
    stamp = stamp_file(filepath, ext='estamp')
    with open(stamp, 'wb'):
        os.utime(stamp, None)

    if os.path.exists(start_stamp):
        os.remove(start_stamp)


def has_start_stamp(filepath):
    """
    Checks if given file has end stamp.
    """
    stamp = stamp_file(filepath, ext='sstamp')
    return os.path.exists(stamp)


def has_end_stamp(filepath):
    """
    Checks if given file has end stamp.
    """
    stamp = stamp_file(filepath, ext='estamp')
    return os.path.exists(stamp)


def remove_original(filepath, filepath_out):
    """
    Removes original file that has been successfully converted and moves the
    newly converted file to its name.
    """
    try:
        os.remove(filepath)
        os.rename(filepath_out, filepath)
    except OSError:
        # This means the file is directory.
        pass


def convert_file(filepath):
    """
    Handles converting of single file. It creates stamps signaling the file is
    being converted and that it was finished.
    """
    path, ext = os.path.splitext(filepath)
    filepath_out = '{}.out.mkv'.format(path)

    if not has_end_stamp(filepath):

        if '.out.' in filepath:  # It is old-style converted file.
            create_end_stamp(filepath)
            return

        if ext not in VIDEO_FORMATS:
            return

        if has_start_stamp(filepath):
            if os.path.exists(filepath_out):
                os.remove(filepath_out)

        try:
            create_start_stamp(filepath)
            print('Converting: {}'.format(filepath))
            with open('{}.convert'.format(path), 'w') as convert_out:
                cmd = [BIN, '-i', filepath, '-sn', '-x265-params', 'crf=25',
                       '-c:v', 'libx265', filepath_out]
                subprocess.check_call(
                    cmd,
                    stdout=convert_out,
                    stderr=convert_out
                )
            create_end_stamp(filepath)
            remove_original(filepath, filepath_out)
        except subprocess.CalledProcessError:
            traceback.print_exc()
            return filepath


def main(path):
    dir_path = os.path.abspath(path)
    files_failed = []

    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.abspath(os.path.join(root, filename))
            failed = convert_file(filepath)

            if failed:
                files_failed.append(filepath)

    for fail in files_failed:
        print('Failed: {}'.format(fail))


def cleanup():
    """
    Removes temporary directory if present.
    """
    global TMP_DIR
    if TMP_DIR:
        try:
            shutil.rmtree(TMP_DIR)
        except PermissionError:
            # We probably don't have access to our own tmp directory, well
            # nothing we can do about it.
            pass


try:
    args = parser.parse_args()
    main(args.path)
except KeyboardInterrupt:
    print('Exiting.')
finally:
    cleanup()

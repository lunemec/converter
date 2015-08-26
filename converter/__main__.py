# -*- encoding: utf-8 -*-

import argparse
import os
import subprocess
import traceback

if os.name == 'posix':
    BIN = r'bin/ffmpeg_unix'
elif os.name == 'nt':
    BIN = r'bin/ffmpeg.exe'

VIDEO_FORMATS = ['.mkv', '.avi', '.mp4']

parser = argparse.ArgumentParser(description='Convert video files to x265.')
parser.add_argument('path', help='Root directory to start converting.')


def create_start_stamp(filepath):
    """
    Creates stamp signaling we started converting given file.
    """
    filename, ext = os.path.splitext(filepath)
    stamp = '{}.stamp'.format(filepath)
    with file(stamp, 'wb') as f:
        os.utime(stamp, None)


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
    path, ext = os.path.splitext(filepath)
    filepath_out = '{}.out.mkv'.format(path)

    if '.out.' in filepath:
        return

    if os.path.isfile(filepath_out):
        return

    if ext not in VIDEO_FORMATS:
        return

    try:
        subprocess.check_call([BIN, '-i', filepath, '-sn', '-x265-params', 'crf=25', '-c:v', 'libx265', filepath_out])
        remove_original(filepath, filepath_out)
    except subprocess.CalledProcessError as e:
        traceback.print_exc()


def main(path):
    dir_path = os.path.abspath(path)

    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            filepath = os.path.abspath(os.path.join(root, filename))
            convert_file(filepath)


args = parser.parse_args()
main(args.path)

# -*- encoding: utf-8 -*-

import os

# TODO - write some unique PC identificator, so you can convert same directory
# using multiple pc's.


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

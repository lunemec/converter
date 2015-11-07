# -*- encoding: utf-8 -*-

import sys


def text(string):
    """
    A helper function for printing to stdout. Some filenames will fail to print
    correctly to terminal. This way the unprintable characters get replaced
    with '?'.
    """
    encoded = string.encode(sys.stdout.encoding, errors='replace')
    decoded = encoded.decode(sys.stdout.encoding)

    print(decoded)

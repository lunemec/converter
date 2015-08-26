# -*- encoding: utf-8 -*-

"""
This is just test of sqlalchemy and home directory resolving.
"""


import sqlite3
import os

DB_FILE = os.path.expanduser('~/.convertdb')


def main():
    conn = sqlite3.connect(DB_FILE)



if __name__ == '__main__':
    main()
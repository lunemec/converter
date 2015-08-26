# -*- encoding: utf-8 -*-

"""
This is just test of sqlalchemy and home directory resolving.
"""


import sqlite3
import os

DB_FILE = os.path.expanduser('~/.convertdb')


def create_table(cursor):
    """
    Creates the table with index on input_path column.
    """
    cursor.execute('''
        CREATE TABLE convert
        (input_path text, output_path text, converted bool)
    ''')
    cursor.execute('CREATE INDEX input_path_index ON convert (input_path);')


def table_exists(cursor):
    """
    Checks wheter the table already exists or should be created.
    """
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
    table = cursor.fetchone()

    return table and 'convert' in table


def main():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if not table_exists(c):
        create_table(c)


if __name__ == '__main__':
    main()

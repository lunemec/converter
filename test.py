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
        (input text, converted bool)
    ''')
    cursor.execute('CREATE INDEX input_index ON convert (input);')


def table_exists(cursor):
    """
    Checks wheter the table already exists or should be created.
    """
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
    table = cursor.fetchone()

    return table and 'convert' in table


def should_convert(cursor, input):
    """
    Checks if we should start converting:
        - if the file exists: previous convert was interrupted, try again
        - we haven't converted yet, convert
    Or we should not:
        - file has already been converted

    @return bool
    """
    cursor.execute('SELECT converted FROM convert WHERE input=?', (input,))
    result = cursor.fetchone()

    if result is None:
        return True

    return not bool(result and result[0])


def started_converting(cursor, input):
    """
    Writes a record into database that we started converting the file.
    """
    cursor.execute('INSERT INTO convert VALUES (?, 0)', (input,))


def finished_converting(cursor, input):
    """
    Writes a record signaling we have completed converting the file.
    """
    cursor.execute('UPDATE convert SET converted=1 WHERE input=?', (input,))


def main():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if not table_exists(c):
        create_table(c)

    for input in ['testfile']:
        if should_convert(c, input):
            started_converting(c, input)
            conn.commit()
            print('Would convert {}'.format(input))
            finished_converting(c, input)
            conn.commit()
        else:
            print('Already converted {}'.format(input))

    conn.close()


if __name__ == '__main__':
    main()

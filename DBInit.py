import sqlite3


def init():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id int(5) NOT NULL,
            username VARCHAR(16) NOT NULL,
            first-name VARCHAR(32) NOT NULL,
            last-name VARCHAR(32),
            password varchar(64) NOT NULL,

            PRIMARY KEY(id)
        )
    ''')

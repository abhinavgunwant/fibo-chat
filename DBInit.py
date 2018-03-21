import sqlite3


def init():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id          int NOT NULL,
            username    VARCHAR(16) NOT NULL,
            first_name  VARCHAR(32) NOT NULL,
            last_name   VARCHAR(32),
            password    varchar(64) NOT NULL,
            PRIMARY KEY(id)
        );''')
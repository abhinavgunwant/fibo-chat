import sqlite3


def init():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(16),
            token VARCHAR(32)
        )
    ''')

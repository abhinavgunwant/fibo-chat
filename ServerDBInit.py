import sqlite3

DB_NAME = 'server-data.db'

def init():
    global DB_NAME
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user (
            first_name  VARCHAR(32) NOT NULL,
            last_name   VARCHAR(32),
            username    VARCHAR(16) NOT NULL,
            email       VARCHAR(64) NOT NULL,
            password    varchar(64) NOT NULL,
            PRIMARY KEY(username)
        );''')
        
        

def insertTable(firstName,lastName,username,email,password):
    global DB_NAME
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO USER(first_name, last_name, username, email, password) VALUES(?,?,?,?,?)",(firstName,lastName,username,email,password))
    conn.commit()
        
        
def loginCheck(username,password):
    global DB_NAME
    conn = sqlite3.connect(DB_NAME)
    result = conn.execute("SELECT * FROM USER WHERE USERNAME = ? AND PASSWORD = ?",(username,password))
    count = len(result.fetchall())
    
    if(count > 0):
        print("Login Successfully")
        return True
            
    else:
        print("You havent registered yet")
        return False

def getAllUsers():
    global DB_NAME
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("select * from user")

    # for row in cursor:


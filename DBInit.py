import sqlite3


def init():
        conn = sqlite3.connect('data.db')
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
        conn = sqlite3.connect('data.db')
        conn.execute("INSERT INTO USER VALUES(?,?,?,?,?)",(firstName,lastName,username,email,password))
        conn.commit()
        
        
def loginCheck(username,password):
        conn = sqlite3.connect('data.db')
        result = conn.execute("SELECT * FROM USER WHERE USERNAME = ? AND PASSWORD = ?",(username,password))
        count = len(result.fetchall())
        
        if(count > 0):
            print("Login Successfully")
            return True
                
        else:
            print("You havent registered yet")
            return False
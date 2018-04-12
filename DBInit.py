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
    
    # user = the 'current' user, who is logged to the system right now!
    # contact = the other user whose chat dialog is opened!
    # direction = 'O' -> Outgoing, 'I' -> Incoming
    cur.execute('''
        CREATE TABLE IF NOT EXISTS message (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user        VARCHAR(32) NOT NULL,
            contact     VARCHAR(32) NOT NULL,
            direction   CHAR(1) NOT NULL,
            text        text,
            datetime    datetime
        );''')

def insertMessage(user, contact, direction, text):
    conn = sqlite3.connect('data.db')
    conn.execute("INSERT INTO MESSAGE (user, contact, direction, text, datetime) VALUES (?, ?, ?, ?, date())",(user, contact, direction, text))
    conn.commit()

def getChats(user, contact):
    conn = sqlite3.connect('data.db')
    chatCur = conn.execute("SELECT user, contact, direction, text, datetime FROM MESSAGE WHERE user = ?, contact = ?", (user, contact))
    prevChats = []
    for row in chatCur:
        prevChats.append({})



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
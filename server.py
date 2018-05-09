import sys
import sqlite3
import json
import _thread
from socket import *

import ServerDBInit

DB_NAME             = 'server-data.db'

dbConn              = sqlite3.connect(DB_NAME)
dbCur               = dbConn.cursor()

ServerDBInit.init()

## default host and port
# host                = "192.168.43.64"
# host                = "127.168.2.75"
host                = "10.20.4.108"
port                = 4447

connectedClients    = {}
contactList         = []

exit                = False

def loadServerConfig():
    global host
    global port
    
    configStr = ''

    with open('server-config.json') as configFile:
        for line in configFile:
            configStr += line

    configJson  = json.loads(configStr)
    host        = configJson['host']
    port        = int(configJson['port'])

def isUserConnected(user):
    global connectedClients
    for key, values in connectedClients.items():
        if key == user:
            return True

    return False

def listener(sock):
    global exit
    print('waiting for client....')
    # gotUser = False
    while not exit:
        sock.listen(1)
        conn,addr = sock.accept()
        print('connected with a client.... listening in new thread....')
        _thread.start_new_thread(listen, (conn, addr,))

## listens a client in a separate thread....
def listen(conn, addr):
    global exit
    global contactList
    global connectedClients
    gotUser = False
    currentUser = ''

    ## The server should now receive the first ever data from the client
    ##  It should be a json having keys either 'login' for login or
    ##  'register' for register...
    while not gotUser:
        firstJsonData = conn.recv(1024).strip().decode()
        firstData = json.loads(firstJsonData)
        if 'type' in firstData:
            if firstData['type'] == 'login':
                print('received a "login" type!')
                respObj = getUser(firstData)
                if respObj['status'] == True:
                    currentUser = respObj['username']
                    connectedClients[currentUser] = [conn, addr]
                    contactRespObj = {
                        'type':     'contactlist',
                        'contacts': contactList,
                        'contactsonline': list(connectedClients.keys())
                    }
                    conn.send(bytes(json.dumps(respObj), 'utf-8'))                
                    # conn.send(bytes(json.dumps(contactRespObj), 'utf-8'))
                    gotUser = True
                    print('!')
                else:
                    conn.send(bytes(json.dumps(respObj), 'utf-8'))
            elif firstData['type'] == 'register':
                print('received a "register" type!')
                respObj = registerUser(firstData)
                conn.send(bytes(json.dumps(respObj), 'utf-8'))
    while not exit:
        data = conn.recv(65535)
        dataText = data.strip().decode('utf-8')
        print('Received from '+currentUser+': '+dataText)
        recData = json.loads(dataText)
        if 'type' in recData and recData['type'] == 'contactlist':
            respObj = {
                'type': 'contactlist',
                'contacts': contactList,
                'contactsonline': list(connectedClients.keys())
            }

            respJson = json.dumps(respObj)
            conn.send(bytes(respJson, 'utf-8'))

        elif ('type' in recData and recData['type'] == 'message' and
            'touser' in recData and isUserConnected(recData['touser'])):
            sendToUser(dataText)

        elif 'type' in recData and recData['type'] == 'exit':
            del connectedClients[recData['username']]
            exit = True
        elif 'type' in recData and recData['type'] == 'keyshare':
            sendToUser(dataText)
        else:
            print('----!!----')

## sends json to the user with the given 'user' id
def sendToUser(jsonDataText):
    recData = json.loads(jsonDataText)
    con = connectedClients[recData['touser']][0]
    print('sending data to: ' + recData['touser'] + ' socket: ' + str(con.getpeername()))
    con.send(bytes(jsonDataText, 'utf-8'))

## Receives the username and password of client when client first connects to the
##      server, hence, the client must send username and password in json format as
##      the first form of data when the connection between server and client is
##      established....
def getUser(userInfo):
    userLoggedIn = False

    if 'username' in userInfo and 'password' in userInfo:
        if ServerDBInit.loginCheck(userInfo['username'], userInfo['password']):
            return {
                'type': 'status',
                'status': True,
                'username': userInfo['username']
            }
        else:
            return {
                    'type': 'status',
                    'status': False
                }

def registerUser(userInfo):
    print('Registering....')
    usrCon  = sqlite3.connect(DB_NAME)
    usrCur  = usrCon.cursor()
    usrCur  = usrCon.execute('SELECT username FROM USER WHERE username = "'+userInfo['username']+'"')
    row     = usrCur.fetchone()

    if row != None:
        if row[0] == userInfo['username']:
            return {'type': 'status', 'status': False, 'message': 'You are already registered!'}
    
    errorMessage        = ''
    registerUserSuccess = False

    if (
        'firstName' in userInfo and 'lastName' in userInfo and 'username' in userInfo 
        and 'email' in userInfo and 'password' in userInfo
    ) == False:
        return {'type': 'status', 'status': False, 'message': 'Form Contains incomplete information'}

    firstName   = userInfo['firstName']
    lastName    = userInfo['lastName']
    username    = userInfo['username']
    email       = userInfo['email']
    password    = userInfo['password']

    if firstName == '' or lastName == '' or username == '' or email == '' or password == '':
        return {'type': 'status', 'status': False, 'message': 'Form Contains incomplete information'}

    ServerDBInit.insertTable(firstName, lastName, username, email, password)

    return {'type': 'status', 'status': True, 'message': 'User registered!', 'username': username}

def loadContactList():
    global dbConn
    contactCur = dbConn.execute('SELECT first_name, last_name, username, email FROM user')
    for row in contactCur:
        contactList.append([row[0], row[1], row[2], row[3]])



def main():
    s=socket(AF_INET, SOCK_STREAM)
    s.bind((host,port))
    print("Listening for connections.. ")

    # loadServerConfig()

    loadContactList()

    _thread.start_new_thread(listener, (s,))

    while not exit:
        if exit:
            print('exiting')

    s.close()

if __name__ == '__main__':
    main()
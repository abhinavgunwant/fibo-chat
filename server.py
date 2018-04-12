import sys
import sqlite3
import json
import _thread
from socket import *

import ServerDBInit

DB_NAME = 'server-data.db'

dbConn = sqlite3.connect(DB_NAME)
dbCur = dbConn.cursor()

ServerDBInit.init()

host="127.168.2.75"
# host="10.20.4.203"
port=4447

connectedClients = {}
contactList = []

exit = False

# def isConnected(clAddr):
#     global connectedClients
#     for keys, arr in connectedClients.iteritems():
#         if clAddr == arr[1]:
#             return True
#     return False

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
        # The server should now receive the first ever data from the client
        # It should be a json having keys either 'login' for login or
        # 'register' for register...
        # while not gotUser:
        #     firstJsonData = conn.recv(1024).strip().decode()
        #     firstData = json.loads(firstJsonData)
        #     if 'type' in firstData:
        #         if firstData['type'] == 'login':
        #             print('received a "login" type!')
        #             respObj = getUser(firstData)
        #             if respObj['status'] == True:
        #                 currentUser = respObj['username']
        #                 connectedClients[currentUser] = [conn, addr]
        #                 gotUser = True
        #             conn.send(bytes(json.dumps(respObj), 'utf-8'))
        #         elif firstData['type'] == 'register':
        #             print('received a "register" type!')
        #             respObj = registerUser(firstData)
        #             # if respObj['status'] == True:
        #             #     currentUser = respObj['username']
        #             #     connectedClients[currentUser] = [conn, addr]
        #             #     gotUser = True
        #             conn.send(bytes(json.dumps(respObj), 'utf-8'))
            
        # print('listening in new thread....')
        _thread.start_new_thread(listen, (conn, addr,))

#listens a client in a separate thread....
def listen(conn, addr):
    global exit
    global contactList
    global connectedClients
    gotUser = False
    currentUser = ''

    # The server should now receive the first ever data from the client
    # It should be a json having keys either 'login' for login or
    # 'register' for register...
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
                        gotUser = True
                    conn.send(bytes(json.dumps(respObj), 'utf-8'))
                elif firstData['type'] == 'register':
                    print('received a "register" type!')
                    respObj = registerUser(firstData)
                    # if respObj['status'] == True:
                    #     currentUser = respObj['username']
                    #     connectedClients[currentUser] = [conn, addr]
                    #     gotUser = True
                    conn.send(bytes(json.dumps(respObj), 'utf-8'))
    while not exit:
        data = conn.recv(65535)
        dataText = data.strip().decode('utf-8')
        print('Received from '+currentUser+': '+dataText)
        recData = json.loads(dataText)
        if 'type' in recData and recData['type'] == 'contactlist':
            # sendContactList()
            respObj = {
                'type': 'contactlist',
                'contacts': contactList,
                'contactsonline': list(connectedClients.keys())
            }

            respJson = json.dumps(respObj)
            conn.send(bytes(respJson, 'utf-8'))

        elif 'touser' in recData and isUserConnected(recData['touser']):
            sendToUser(dataText)

        elif 'type' in recData and recData['type'] == 'exit':
            del connectedClients[recData['username']]
            exit = True

# sends json to the user with the given 'user' id
def sendToUser(jsonDataText):
    recData = json.loads(jsonDataText)
    con = connectedClients[recData['touser']][0]
    con.send(bytes(jsonDataText, 'utf-8'))

# Receives the username and password of client when client first connects to the
# server, hence, the client must send username and password in json format as
# the first form of data when the connection between server and client is
# established....
def getUser(userInfo):
    userLoggedIn = False
    # while not userLoggedIn:
        # data = conn.recv(1024)
        # userTextJson = data.strip().decode()
        # userInfo = json.loads(userTextJson)

    if 'username' in userInfo and 'password' in userInfo:
        if ServerDBInit.loginCheck(userInfo['username'], userInfo['password']):
            return {
                    'type': 'status',
                    'status': True,
                    'username': userInfo['username']
                }
            # conn.send(bytes(statusJSON, 'utf-8'))
            # userLoggedIn = True

            # connectedClients[userText] = [conn, addr]
            # return userInfo['username']
        else:
            return {
                    'type': 'status',
                    'status': False
                }
            # conn.send(bytes(statusJSON, 'utf-8'))

def registerUser(userInfo):
    print('Registering....')
    usrCon = sqlite3.connect(DB_NAME)
    usrCur = usrCon.cursor()
    usrCur = usrCon.execute('SELECT username FROM USER WHERE username = "'+userInfo['username']+'"')
    row = usrCur.fetchone()

    # print(row)

    if row != None:
        if row[0] == userInfo['username']:
            return {'type': 'status', 'status': False, 'message': 'You are already registered!'}
    
    errorMessage = ''
    registerUserSuccess = False

    if (
        'firstName' in userInfo and 'lastName' in userInfo and 'username' in userInfo 
        and 'email' in userInfo and 'password' in userInfo
    ) == False:
        return {'type': 'status', 'status': False, 'message': 'Form Contains incomplete information'}

    firstName = userInfo['firstName']
    lastName = userInfo['lastName']
    username = userInfo['username']
    email = userInfo['email']
    password = userInfo['password']

    if firstName == '' or lastName == '' or username == '' or email == '' or password == '':
        return {'type': 'status', 'status': False, 'message': 'Form Contains incomplete information'}

    ServerDBInit.insertTable(firstName, lastName, username, email, password)

    # con = sqlite3.connect()

    return {'type': 'status', 'status': True, 'message': 'User registered!', 'username': username}

def loadContactList():
    global dbConn
    contactCur = dbConn.execute('SELECT first_name, last_name, username, email FROM user')
    for row in contactCur:
        contactList.append([row[0], row[1], row[2], row[3]])


s=socket(AF_INET, SOCK_STREAM)
s.bind((host,port))
print("Listening for connections.. ")

loadContactList()

_thread.start_new_thread(listener, (s,))

while not exit:
    if exit:
        print('exiting')

s.close()

# def sendContactList():
    
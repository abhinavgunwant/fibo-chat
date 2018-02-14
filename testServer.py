import socket
import threading
import queue
import time
import json

import DBInit

loopExit = False

requestQueue = queue.PriorityQueue()

class Server:
    def __init__(self):
        self.serverSocket = None
        self.exit = False
        self.hostName = socket.gethostname()
        self.port = 16048

    def start(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.hostName, self.port))
        self.serverSocket.listen(65536)

        self.loop()

    def loop(self):
        global loopExit
        global requestQueue
        print('in loop.....')

        con, cl_addr = self.serverSocket.accept()
        self.serve = Serve(con, cl_addr)
        self.serve.start()

        try:
            while not loopExit:
                data = (con.recv(65536)).decode('utf-8')
                if data == 'exit':
                    print('explicit exit....')
                    loopExit = True
                    exit()

                if data:
                    print(data)
                    reqObj = json.loads(data)
                    priority = 1
                    if reqObj['request-type'].upper() == 'EXIT':
                        priority = 0

                    requestQueue.put((priority, reqObj))
        finally:
            con.close()

class Serve(threading.Thread):
    def __init__(self, connection, clientAddress):
        threading.Thread.__init__(self)
        self.connection = connection
        self.clientAddress = clientAddress

    def run(self):
        global loopExit
        global requestQueue
        try:
            while not loopExit:
                if requestQueue.empty() == True:
                    time.sleep(1)
                reqObj = requestQueue.get()
                if (reqObj['request-type']).upper() == 'EXIT':
                    loopExit = True
                    break
                if (reqObj['request-type']).upper() == 'REGISTER':

        finally:
            print('Exiting....')

class TextPrompt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def start(self):
        global loopExit
        text = ''
            while True:
            text = input()
            if text == 'exit':
                loopExit = True
                break

def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    main()

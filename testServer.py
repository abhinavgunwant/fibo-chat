import socket
import threading

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
        print('in loop.....')
        while not self.exit:
            con, cl_addr = self.serverSocket.accept()
            # try:
            #     while True:
            #         data = con.recv(65536)
            #         if data == b'exit':
            #             print('explicit exit....')
            #             exit()
            #         if data:
            #             print(data)
            # finally:
            #     con.close()
            Serve(con, cl_addr).start()

class Serve(threading.Thread):
    def __init__(self, connection, clientAddress):
        threading.Thread.__init__(self)
        self.connection = connection
        self.clientAddress = clientAddress

    def run(self):
        try:
            while True:
                data = self.connection.recv(65536)
                if data == b'exit':
                    print('explicit exit....')
                    exit()
                if data:
                    print(data)
        finally:
            self.connection.close()


def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    main()

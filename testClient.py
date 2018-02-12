import socket

# data = 'This is sample data!'
# data = 'exit'

data = input('Enter text for this thread: ')


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((socket.gethostname(), 16048))

    def send(self, data):
        self.sock.send(str.encode(data))

def main():
    global data
    client = Client()
    client.send(data)


if __name__ == '__main__':
    main()

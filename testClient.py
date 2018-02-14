import socket
import json

request = {
    'request-type': "REGISTER",
    'username': 'abhii',
    'password': 'password',
    'first-name': 'Abhinav',
    'middle-name': None,
    'last-name': 'Gunwant',
    'city': 'Haldwani',
    'coutntry': 'India'
}

data = json.dumps(request)

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

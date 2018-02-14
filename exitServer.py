import socket
import json

request = {
    'request-type': 'exit'
}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(), 16048))
sock.send(str.encode(json.dumps(request)))

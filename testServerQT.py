import sys
import base64
from PyQt5.QtCore import QUrl,  QObject, pyqtSlot, QCoreApplication, QTimer, QByteArray, QIODevice, QDataStream
from PyQt5.QtNetwork import QTcpSocket, QTcpServer, QHostAddress,  QNetworkProxy, QNetworkRequest, QNetworkAccessManager

class Server:
    def __init__(self):
        self.server = None

    def start(self):
        self.server = QTcpServer(None)
        self.server.listen(QHostAddress.Any, 8000)
        self.server.newConnection.connect(self.newConnection)

    def newConnection(self):
        print('new')
        self.currClientConnection = self.server.nextPendingConnection()
        self.readStream = QDataStream(self.server)



def main():
    app = QCoreApplication(sys.argv)
    server = Server()
    server.start()
    print('Server Running...')
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import socket
import threading

class Server:
       
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
       
        self.sock.bind(('127.0.0.1', 8080))
        self.sock.listen(10)

    def handler(self, conn, addr):
        while True:
            data = conn.recv(1024)
            for connection in self.connections:
                connection.send(data)
                print(data)
            if not data:
                break

    def run(self):
        while True:
            conn ,addr = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(conn, addr))
            cThread.daemon = True
            cThread.start()
            self.connections.append(conn)
            print(self.connections)


server = Server()
server.run()

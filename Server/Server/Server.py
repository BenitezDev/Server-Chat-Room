import socket
import threading
import argparse

class Server:
       
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self, address, port, connections):
        self.sock.bind((address, port))
        self.sock.listen(connections)
        print(address, port, connections)

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


parser = argparse.ArgumentParser()
parser.add_argument('--address',    type=str, required=False, help='The address of the server'        ,  default='127.0.0.1')
parser.add_argument('--port',       type=int, required=False, help='The port of the server'           ,  default=8080       )
parser.add_argument('--conections', type=int, required=False, help='The maximum number of connections',  default=10         )
args = parser.parse_args()

server = Server(args.address, args.port, args.conections)
server.run()


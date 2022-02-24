import socket
import threading
import argparse
import time

buffer_size = 1024

class Server:
       
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients = []
    nicknames = []

    def __init__(self, address, port, connections):
        self.sock.bind((address, port))
        self.sock.listen(connections)
        print(f"Server listening in {address}:{port}")

    # Sending Messages To All Connected Clients
    def broadcast(self, message):
        for client in self.clients:
            client.send(message.decode('ascii'))

    # Handling Messages From Clients
    def handle(self, client):
        while True:
            try:
                # Broadcasting Messages
                # here is error :(
                message = client.recv(buffer_size).decode('ascii')
                print(message)
                self.broadcast(message)

            except:
                # Removing And Closing Clients
                index = self.clients.index(client)
                # self.broadcast('{} left!'.format(nickname).encode('ascii'))
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)


    # Receiving / Listening Function
    def receive(self):
        while True:
            # Accept new connections
            client, address = self.sock.accept()
            print("Connected with {}".format(str(address)))

            # Store Nickname            
            nickname = client.recv(buffer_size).decode('ascii')

            if nickname not in self.nicknames:
                print(nickname, "enter the chat!")
                self.nicknames.append(nickname)
                self.clients.append(client)
                client.send('Connected to server!'.encode('ascii'))
            else:
                client.send('Nickname already in use.'.encode('ascii'))
                continue

            # Print And Broadcast Nickname
            # self.broadcast("{} joined!".format(nickname).encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


parser = argparse.ArgumentParser()
parser.add_argument('--address',    type=str, required=False, help='The IP address of the server'     ,  default='127.0.0.1')
parser.add_argument('--port',       type=int, required=False, help='The port of the server'           ,  default=8080       )
parser.add_argument('--conections', type=int, required=False, help='The maximum number of connections',  default=10         )
args = parser.parse_args()

server = Server(args.address, args.port, args.conections)
server.receive()


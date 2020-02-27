__author__ = "jacksonsr45@gmail.com"

import socket
import select
from app.config import conn

class Server:
    def __init__(self):
        self.HEADER_LENGTH = conn['HEADER_LENGTH']
        self.IP = conn['IP']
        self.PORT = conn['PORT']
        self.sockets_list = []
        self.clients = {}


        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.IP, self.PORT))

        self.server_socket.listen()

        self.sockets_list.append(self.server_socket)

        self.__run_server()

        
    def __run_server(self):
        while True:
            read_sockets, _, exception_socket = select.select( self.sockets_list, [], self.sockets_list)

            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.user = self.receive_message(client_socket)

                    if self.user is False:
                        continue

                    self.sockets_list.append(self.client_socket)

                    clients[self.client_socket] = self.user
                    print(f"Accepde new connection from {self.client_address[0]}:{self.client_address[1]} username: {self.user['data'].decode('utf-8')}")

                else:
                    self.message = self.receive_message(notified_socket)

                    if self.message is False:
                        print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                        self.sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue

                    self.user = clients[notified_socket]
                    print(f"Received message from {self.user['data'].decode('utf-8')}:{self.message['data'].decode('utf-8')}")

                    for self.client_socket in clients:
                        if self.client_socket != notified_socket:
                            self.client_socket.send(self.user['header'] + self.user['data'] + self.message['header'] + self.message['data'])
                            
            for notified_socket in exception_socket:
                self.sockets_list.remove(notified_socket)
                del self.client_socket[notified_socket]

    
    
    def receive_message(client_socket):
        try:
            message_header = client_socket.recv(self.HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode("utf-8").strip())
            return {'header': message_header, 'data': client_socket.recv(message_length)}
        except:
            return False
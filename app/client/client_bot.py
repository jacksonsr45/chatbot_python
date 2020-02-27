__author__ = "jacksonsr45@gmail.com"
import socket
import select
import errno
import sys
from app.config import conn
from app.config import username


class Client:
    def __init__(self):
        self.HEADER_LENGTH = conn['HEADER_LENGTH']
        self.IP = conn['IP']
        self.PORT = conn['PORT']
        self.display_message = ""

        self.my_username = username['name']

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(False)

        self.username = self.my_username.encode("utf-8")
        self.username_header =f"{len(self.username):<{self.HEADER_LENGTH}}".encode("utf-8")
        self.teste = self.client_socket.send(self.username_header + self.username)

        
        
    
    def __send_message__(self):
        while True:

            self.message = input(f"{self.my_username} > ")

            
            self.message = self.message.encode("utf-8")
            self.message_header = f"{len(self.message):<{self.HEADER_LENGTH}}".encode("utf-8")
            self.client_socket.send(self.message_header + self.message)

            print(self.message_header + self.message)

    
    def __recv_message__(self):
        while True:
            try:
                while True:
                    self.username_header = self.client_socket.recv(self.HEADER_LENGTH)
                    
                    if not len(self.username_header):
                        print("connection close by the server")
                        sys.exit()
                    
                    self.username_length = int(self.username_header.decode("utf-8").strip())
                    self.username = self.client_socket.recv(self.username_length).decode("utf-8")

                    self.message_header = self.client_socket.recv(self.HEADER_LENGTH)
                    self.message_length = int(self.message_header.decode("utf-8").strip())
                    self.recv_message = self.client_socket.recv(self.message_length).decode("utf-8")

                    self.__get_message(self.username, self.recv_message)         

                    print(self.display_message)

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error', str(e))
                    sys.exit()
                continue
            
            except Exception as e:
                print('General erron', str(e))
                sys.exit()




    def __get_message(self, username, message):
        self.display_message = f"{username} > {message}"
        return self.display_message



    def return_message(self):
        message = self.display_message
        print(self.display_message)
        return message
        
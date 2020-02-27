__author__ = "jacksonsr45@gmail.com"
import socket
import select
import errno
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from app.config import conn
from app.config import cst
from app.config import name_bot

class Chat_Bot:
    def __init__(self):
        HEADER_LENGTH = conn['HEADER_LENGTH']
        IP = conn['IP']
        PORT = conn['PORT']

        # config the chatterbot
        bot = ChatBot('Chatbot 1')
        trainers = ListTrainer(bot)
        conversation = cst
        trainers.train(conversation)

        # Name from bot
        my_username = name_bot['name']

        # Config fron socket 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)

        username = my_username.encode("utf-8")
        username_header =f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
        teste = client_socket.send(username_header + username)


        while True:
            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)
                    
                    if not len(username_header):
                        print("connection close by the server")
                        sys.exit()
                    
                    # Get message by cliente by socket 
                    username_length = int(username_header.decode("utf-8").strip())
                    username = client_socket.recv(username_length).decode("utf-8")

                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode("utf-8").strip())
                    recv_message = client_socket.recv(message_length).decode("utf-8")

                    print(f"{username} > {recv_message}") 

                    # bot get messagem and generate a message    
                    user_input = recv_message
                    bot_response = bot.get_response(user_input)

                    # Receive by client and send message from cliente 
                    value = f"{bot_response}"
                    recv_message = value.encode("utf-8")
                    message_header = f"{len(recv_message):<{HEADER_LENGTH}}".encode("utf-8")
                    client_socket.send(message_header + recv_message)

                    self.__set_display_message(username, recv_message)         



            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error', str(e))
                    sys.exit()
                continue
            
            except Exception as e:
                print('General erron', str(e))
                sys.exit()

    

    def __set_display_message(self, username, message):
        self.display_message = f"{username} > {message}"
        return self.display_message



    def return_message(self):
        message = self.display_message
        print(self.display_message)
        return message
__author__ = "jacksonsr45@gmail.com"
import socket
import select
import errno
import sys
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from app.config import conn

class Chat_Bot:
    def __init__(self):
        HEADER_LENGTH = conn['HEADER_LENGTH']
        IP = conn['IP']
        PORT = conn['PORT']


        bot = ChatBot('Chatbot 1')
        trainers = ListTrainer(bot)

        conversation = [
            'helo',
        ]

        trainers.train(conversation)

        my_username = "Chatbot 1"
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)

        username = my_username.encode("utf-8")
        username_header =f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
        teste = client_socket.send(username_header + username)


        while True:
            #message = ""
            message = input(f"{my_username} > ")

            if message:
                message = bot.get_response(query)
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
                client_socket.send(message_header + message)

            try:
                while True:
                    username_header = client_socket.recv(HEADER_LENGTH)
                    
                    if not len(username_header):
                        print("connection close by the server")
                        sys.exit()
                    
                    username_length = int(username_header.decode("utf-8").strip())
                    username = client_socket.recv(username_length).decode("utf-8")

                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode("utf-8").strip())
                    message = client_socket.recv(message_length).decode("utf-8")

                    print(f"{username} > {message}") 

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error', str(e))
                    sys.exit()
                continue
            
            except Exception as e:
                print('General erron', str(e))
                sys.exit()
Chat_Bot()
__author__ = "jacksonsr45@gmail.com"

from app.client.client_bot import Client

class Teste_Client:
    def __init__(self):
        Client().__send_message__()

if __name__ == "__main__":
    Teste_Client()
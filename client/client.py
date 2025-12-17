import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 8080


class Client:

    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.talk_to_server()

        print(f"\033[34mClient:\033[0m Connected at {host}:{port}")

    def talk_to_server(self):
        Thread(target = self.receive_message).start()
        self.send_messages()

    def receive_message(self):
        while True:
            message = self.sock.recv(1024).decode()
            if not message:
                break
            print(f"\033[33mClient:\033[0m {message}")

    def send_messages(self):
        while True:
            client_message = input("")
            self.sock.send(client_message.encode())

Client(HOST, PORT)

# # create a new socket object, AF_INET for IPv4 and SOCK_STREAM for TCP
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))
#
# # sending in bytes not strings
# sock.send(b'Hello, server!')
# print(sock.recv(1024).decode())
#
# def receive_msg():
#     while True:
#         el = sock.recv(1024).decode()
#         print(el)
#         return el
#
# # Creating multi thread (listening)
# thread = threading.Thread(
#     # What the thread will do when the thread has started
#     target=receive_msg
# )
# thread.start()
#
# # Main Thread (talking)
# while True:
#     msg = input("> ")
#     sock.send(msg)
#     receive_msg()

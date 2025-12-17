import socket
from threading import Thread
# from server.client_handler import client_handler

class Server:

    clients = [] # für später

    def __init__(self, host, port):
        # create a new socket object, AF_INET for IPv4 and SOCK_STREAM for TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()

        print(f"\033[31mServer:\033[0m startet at {host}:{port}")

        client_conn, addr = self.sock.accept()
        self.talk_to_client(client_conn)

    # method to talk to client
    def talk_to_client(self, client_conn):
        # args muss ein tuple sein, daemon auf true setzten damit das Programm abgewürgt werden kann
        Thread(target = self.receive_message, args=(client_conn,), daemon=True).start()
        self.send_message(client_conn)

    # method to receive message from client
    def receive_message(self, client_conn):
        while True:
            message = client_conn.recv(1024).decode()
            print(f"\033[34mUserX:\033[0m {message}")
            client_conn.sendall(message.encode())

    # method to send message to client
    def send_message(self, client_conn):
        while True:
            server_message = input("")
            if server_message == "exit":
                break
            print(f"\033[31mServer:\033[0m {server_message}")
            client_conn.send(server_message.encode())


Server('127.0.0.1', 8080)

# while True:
#     conn, addr = sock.accept()
#     print(f'Connected with {addr}')
#     # handler for each client
#     client_handler(conn, addr)
#
#     # start a new thread for each client
#     thread = threading.Thread(target=client_handler, args=(conn, addr))
#     thread.start()



# while True:
#     data = conn.recv(1024) # get data from a client in buffer size of 1024 bytes
#     if not data:
#         break
#     print(f'Received {data.decode()} from {addr}')
#     conn.sendall(data)





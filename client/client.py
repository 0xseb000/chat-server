import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 8080

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))

        print(f"\033[34mClient:\033[0m Connected at {host}:{port}")
        print("Hinweis: Gib zuerst den Raumnamen ein (z.B. 'raum1').")
        print("Später kannst du mit '/join raum2' den Raum wechseln.")

        self.talk_to_server()

    def talk_to_server(self):
        # Thread zum Empfangen
        Thread(target=self.receive_message, daemon=True).start()
        # Im Hauptthread senden
        self.send_messages()

    def receive_message(self):
        while True:
            message = self.sock.recv(1024).decode()
            if not message:
                print("\033[31mVerbindung zum Server verloren.\033[0m")
                break
            print(f"\033[33mMessage:\033[0m {message}", end="")  # \n ist schon drin

    def send_messages(self):
        while True:
            client_message = input("")

            if client_message == "exit":
                self.sock.close()
                break

            self.sock.send(client_message.encode())

Client(HOST, PORT)

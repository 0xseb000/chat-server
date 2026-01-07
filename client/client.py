import socket
from threading import Thread


class Client:

    def __init__(self, host, port):
        # Socket erzeugen und direkt mit dem Server verbinden
        self.sock = socket.socket()
        self.sock.connect((host, port))

        # Kleine Statusmeldung für den Nutzer, besseres UX
        print(f"\033[34mClient:\033[0m Connected at {host}:{port}")
        print("Hinweis: Gib zuerst den Raumnamen ein (z.B. 'main').")
        print("Später kannst du mit '/cd <raumname>' den Raum wechseln.")

        # Startet die Client Logik (Empfangen und Senden)
        self.talk_to_server()

    def talk_to_server(self):
        # Ein Thread empfängt Nachrichten vom Server (receive_message)
        # Der Hauptthread übernimmt die Eingabe vom Nutzer (send_messages)
        Thread(target=self.receive_message, daemon=True).start()
        self.send_messages()

    def receive_message(self):
        # Läuft in eigenem Thread
        # Wartet auf neue Nachrichten vom Server und gibt diese aus
        while True:
            message = self.sock.recv(1024).decode()
            # Wenn Server die Verbindung trennt, recv liefert nicht mehr Daten
            if not message:
                print("\033[31mVerbindung zum Server verloren.\033[0m")
                break
            print(f"\033[33mMessage:\033[0m {message}", end="")

    def send_messages(self):
        # Läuft im Hauptthread
        # Liest Nachrichten vom Nutzer ein und sendet diese an den Server
        while True:
            client_message = input("")

            if client_message == "exit":
                self.sock.close()
                break

            self.sock.send(client_message.encode())

Client('127.0.0.1', 8080)

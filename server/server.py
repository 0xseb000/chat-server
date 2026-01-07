import socket
from threading import Thread


class Server:

    def __init__(self, host, port):
        # Räume: Jeder Raum hat eine eigene Liste von Clients
        # Ein Client wird durch seinen Socket repräsentiert
        self.rooms = {
            "main": [],
            "lounge": [],
            "coffee-break": []
        }

        # Merkt sich, in welchem Raum welcher Client aktuell ist
        self.client_rooms = {}

        # Server Socket vorbereiten, hier entsteht der Haupteingang
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))   # Adresse + Port reservieren
        self.sock.listen()             # Server in "Wartemodus" versetzen

        print(f"\033[31mServer:\033[0m startet at {host}:{port}")
        print("Verfügbare Räume: main, lounge, coffee-break")

        # Separater Thread, der ausschliesslich neue Clients annimmt
        # Durch daemon blockiert accept() nicht den Hauptthread
        Thread(target=self.accept_clients, daemon=True).start()

        # Der Hauptthread bleibt für Server Eingaben reserviert (Admin)
        self.handle_console()


    def accept_clients(self):
        # Diese Schleife läuft dauerhaft und wartet auf neue Verbindungen
        while True:
            # Sobald sich ein Client verbindet, erzeugt accept()
            # einen neuen Socket NUR für diese Verbindung
            client_conn, addr = self.sock.accept()
            print(f"\033[32mNeuer Client verbunden:\033[0m {addr}")

            # Für jeden Client wird ein eigener Thread gestartet.
            # Dadurch können mehrere Clients gleichzeitig chatten.
            Thread(
                target=self.handle_client,
                args=(client_conn, addr),
                daemon=True
            ).start()


    def handle_client(self, client_conn, addr):
        # Begrüssungsnachricht direkt nach Verbindungsaufbau
        welcome = (
            "Willkommen auf dem Chat Server!\n"
            "Verfügbare Räume: main, lounge, coffee-break\n"
            "Bitte gib den Raumnamen ein (z.B. 'lounge'):\n> "
        )
        client_conn.sendall(welcome.encode())

        # Der erste Input des Clients bestimmt den Raum
        room_choice = client_conn.recv(1024).decode().strip().lower()

        # Wenn Raum ungültig, dann automatisch nach raum1 schicken
        if room_choice not in self.rooms:
            client_conn.sendall(
                "Unbekannter Raum. Du kommst in 'main'.\n".encode()
            )
            room_choice = "main"

        # Client wird dem Raum zugeordnet
        self.rooms[room_choice].append(client_conn)
        self.client_rooms[client_conn] = room_choice

        # Info für den Client selbst
        client_conn.sendall(
            f"Du bist jetzt in '{room_choice}'. "
            f"Mit '/cd name-des-raums' kannst du den Raum wechseln.\n".encode()
        )

        # Alle anderen im Raum erfahren, dass jemand beigetreten ist
        self.broadcast(
            room_choice,
            f"[System] User {addr} hat den Raum betreten.",
            sender=client_conn
        )

        # Ab hier läuft die eigentliche Chat-Schleife
        while True:
            # Warten auf nächste Nachricht vom Client
            data = client_conn.recv(1024)

            # Wenn nichts mehr kommt → Verbindung wurde geschlossen
            if not data:
                break

            message = data.decode().strip()

            # Wenn der User den Raum wechseln möchte
            if message.startswith("/cd "):
                new_room = message.split(" ", 1)[1].strip().lower()
                self.change_room(client_conn, addr, new_room)
                continue

            # Nachsehen, in welchem Raum der Client aktuell ist
            current_room = self.client_rooms.get(client_conn)

            # Falls aus irgendeinem Grund kein Raum zugeordnet ist
            if current_room is None:
                client_conn.sendall(
                    "Du bist in keinem Raum. Nutze z.B. '/cd main'.\n".encode()
                )
                continue

            # Log-Ausgabe im Server-Terminal
            print(f"\033[34mUser {addr} @ {current_room}:\033[0m {message}")

            # Nachricht an alle anderen Clients im Raum senden
            self.broadcast(
                current_room,
                f"User {addr}: {message}",
                sender=client_conn
            )

        # Wenn der Chat-Loop endet → Client sauber entfernen
        self.remove_client(client_conn, addr)


    def change_room(self, client_conn, addr, new_room):
        # Aktuellen Raum ermitteln
        current_room = self.client_rooms.get(client_conn)

        # Ungültiger Raumname?
        if new_room not in self.rooms:
            client_conn.sendall(
                f"[System] Raum '{new_room}' existiert nicht. "
                "Verfügbare Räume: main, lounge, coffee-break\n".encode()
            )
            return

        # Wenn der Nutzer schon dort ist, muss nichts passieren
        if current_room == new_room:
            client_conn.sendall(
                f"[System] Du bist bereits in '{new_room}'.\n".encode()
            )
            return

        # Aus altem Raum austragen
        if current_room and client_conn in self.rooms[current_room]:
            self.rooms[current_room].remove(client_conn)

        # In neuen Raum eintragen
        self.rooms[new_room].append(client_conn)
        self.client_rooms[client_conn] = new_room

        # Bestätigung für den Client
        client_conn.sendall(
            f"[System] Du bist jetzt in '{new_room}'.\n".encode()
        )

        # System-Nachrichten für beide Räume
        if current_room:
            self.broadcast(
                current_room,
                f"[System] User {addr} hat den Raum verlassen.",
                sender=client_conn
            )

        self.broadcast(
            new_room,
            f"[System] User {addr} ist dem Raum beigetreten.",
            sender=client_conn
        )


    def broadcast(self, room_name, message, sender=None):
        # Kopie der Raumliste, falls jemand die Liste währenddessen verändert
        clients = list(self.rooms.get(room_name, []))

        # Nachricht an alle Clients ausser dem Sender
        for client in clients:
            if client is sender:
                continue
            client.sendall((message + "\n").encode())


    def remove_client(self, client_conn, addr):
        # Raumzuordnung entfernen
        room = self.client_rooms.pop(client_conn, None)

        # Falls der Client noch in einem Raum war → austragen
        if room and client_conn in self.rooms[room]:
            self.rooms[room].remove(client_conn)

        # Info für die anderen Nutzer
        if room:
            self.broadcast(room, f"[System] User {addr} hat die Verbindung getrennt.")

        # Verbindung schliessen
        client_conn.close()
        print(f"\033[31mClient getrennt:\033[0m {addr}")


    def handle_console(self):
        # Server Admin kann hier Nachrichten eingeben oder 'exit' tippen
        while True:
            server_message = input("")

            # Server beenden
            if server_message == "exit":
                print("\033[31mServer:\033[0m wird beendet...")
                self.sock.close()
                break

            # Nachricht an alle Räume schicken
            print(f"\033[31mServer (an alle Räume):\033[0m {server_message}")

            for room_name in list(self.rooms.keys()):
                self.broadcast(room_name, f"Server: {server_message}")


# Einstiegspunkt — hier startet der Server
Server('127.0.0.1', 8080)


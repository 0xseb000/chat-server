# Multi-Room Chat Server

Ein kleiner, leichtgewichtiger Chat-Server mit Unterstützung für mehreren Chat Räumen.
Clients verbinden sich über das Terminal, wählen beim ersten Verbindungsaufbau einen Raum
und können anschliessend Nachrichten innerhalb dieses Raums senden oder per Befehl
den Raum wechseln. Der Server unterstützt mehrere parallele Clients.

Der Chat basiert auf **IPv4 (AF_INET)** und verwendet das **TCP-Protokoll (SOCK_STREAM)**.
Damit läuft die Kommunikation zuverlässig verbindungsorientiert. Jede Nachricht wird
über eine stabile TCP Verbindung zwischen Client und Server übertragen.

Der Server arbeitet **multithreaded**:
Für jeden verbundenen Client wird ein eigener Thread gestartet, sodass mehrere Benutzer
gleichzeitig schreiben, empfangen und die Räume wechseln können.

---

## Hinweise

- Der Server läuft standardmässig auf **Host 127.0.0.1** und **Port 8080**.
- Der Server kann Nachrichten an alle Räume gleichzeitig senden.
- Nachrichten von Clients werden nur an Clients im selben Raum gesendet.
- Benutzer werden automatisch benachrichtigt, wenn jemand einen Raum betritt oder verlässt.
- Jeder Client läuft in einem eigenen Terminalfenster.
- Der Server kann mehrere Clients gleichzeitig bedienen.

---

## Voraussetzungen

Python 3.x und freie Port-Verbindung auf 127.0.0.1:8080

---

## Verwendung
In das Verzeichnis des Projekts wechseln.

### Server starten
Der Server startet und wartet auf eingehende Verbindungen.

    python3 ./server/server.py


### Einen oder mehrere Clients starten
Für jeden Client ein eigenes Terminalfenster öffnen und folgende Befehle eingeben:

    python3 ./client/client.py


---

### Beim ersten Verbindungsaufbau mit Client, Raum auswählen

Mögliche Beispiele:

    main
    lounge
    coffee-break

Erst danach beginnt der Chat.

---

### Zwischen Räumen wechseln

    /cd <raumname>

**Beispiele:**

    /cd main
    /cd lounge
    /cd coffee-break

---

## Befehlsliste

| Befehl            | Beschreibung                                      |
|------------------|----------------------------------------------------|
| /cd <raumname>   | In einen anderen Raum wechseln                     |
| exit             | Verbindung trennen (Client) oder Server beenden    |

---
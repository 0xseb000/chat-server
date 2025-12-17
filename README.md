
### Aus der Root 
Server muss zuerst gestartet werden.
```bash
python3 ./server/server.py
```
Danach Client starten.
```bash
python3 ./server/server.py
python3 ./client/client.py
```

Nun kann gechattet werden.

[//]: # (Der server.py nimmt nur die Verbindung an und startet den Handler.)

[//]: # (Der Handler bearbeitet die Verbindung.)

[//]: # (Client sendet und empfängt Daten.)

[//]: # (__init__.py macht Server und Client directory zu einem Python Package. Dadurch muss jedoch der Server von der root aus)
[//]: # (gestartet werden und zwar als Modul:)


Der server.py nimmt nur die Verbindung an und startet den Handler.
client_handler.py ist für die Kommunikation zwischen Client und Server zuständig.

__init__.py macht Server und Client directory zu einem Python Package. Dadurch muss jedoch der Server von der root aus
gestartet werden und zwar als Modul:

```bash
python3 -m server.server
```
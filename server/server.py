import socket
from server.client_handler import client_handler

host = '127.0.0.1'
port = 8080

sock = socket.socket()
sock.bind((host, port))
sock.listen()

print(f'Server is running on {host}:{port}')

# when connection: creates a new socket object (conn) and address (addr)
conn, addr = sock.accept()

client_handler(conn, addr)

# while True:
#     data = conn.recv(1024) # get data from a client in buffer size of 1024 bytes
#     if not data:
#         break
#     print(f'Received {data.decode()} from {addr}')
#     conn.sendall(data)





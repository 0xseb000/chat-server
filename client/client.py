import socket

HOST = '127.0.0.1'
PORT = 8080

# create a new socket object, AF_INET for IPv4 and SOCK_STREAM for TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# sending in bytes not strings
sock.send(b'Hello, server!')
print(sock.recv(1024).decode())

sock.close()
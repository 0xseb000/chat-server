
clients = []

def client_handler(conn, addr):

    print(f"Connected with {addr}")
    clients.append(conn)

    while True:
        data = conn.recv(1024)
        if not data:
            conn.close()
            break
        conn.sendall(data)
        # logging what is received
        print("Received", data.decode())

    clients.remove(conn)
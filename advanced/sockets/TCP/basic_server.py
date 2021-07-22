import socket
import threading


#running locally
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
print(f"HOSTNAME: {hostname}")
print(f"HOST: {HOST}")
PORT = 10098

"""
Usado para criar TCP socket: socket.SOCK_STREAM
Usado para criar UDP socket: socket.SOCK_DGRAM

Utiliza protocolo IPv4: AF_INET
Utiliza protocolo IPv6: AF_INET6
"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            # receives 1024 bytes
            message = client.recv(1024)
            broadcast(message)
        except Exception:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:

        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f'{nickname} joined the chat!'.encode("ascii"))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()

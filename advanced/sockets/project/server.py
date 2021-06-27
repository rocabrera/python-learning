import socket
import threading
# running locally
from message import Message

import json


class Servidor:

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 10098
    BUFFERSIZE = 1024

    def __init__(self):
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.HOST, self.PORT))
        self.peers = {}  # Python Dict são thread

    def _receive(self):

        while True:
            try:
                data, peer = self.UDPServerSocket.recvfrom(self.BUFFERSIZE)

                recv_msg = json.loads(data.decode('utf-8'))  # Transforma json em dict

                # Criar uma thread para cada requisição de um cliente
                thread = threading.Thread(
                    target=self._handle_request, args=(peer, recv_msg))

                thread.start()
                thread.join()

            except KeyboardInterrupt:
                """
                No futuro eu devo tirar o client se algum erro acontecer
                """
                print()
                print("#" * 64)
                print(self.peers)
                print("#" * 64)
                self.UDPServerSocket.close()
                break

    def _handle_request(self, peer, recv_msg):

        request, msg = recv_msg["message"].split(':')

        if request == "JOIN":
            return self._handle_join(peer, msg)

        elif request == "LEAVE":
            return self._handle_leave(peer)

        elif request == "ALIVE_OK":
            self._handle_alive()

    def _handle_join(self, peer, msg):
        peer_address, peer_port = peer
        file_lst = msg.strip()
        if peer not in self.peers:
            self.peers[peer] = file_lst.split()  # Grava o peer no servidor
            print(f"Peer [{peer_address}]:{peer_port} adicionado com arquivos {file_lst}")
            msg = Message("JOIN_OK\n")
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer)
        else:
            msg = Message("Você já está conectado\n")
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer)
            print(f"Peer [{peer_address}]:{peer_port} já está conectado")

    def _handle_leave(self, peer):
        if peer in self.peers:
            self.peers.pop(peer)  # Retira o peer do servidor
            msg = Message("LEAVE_OK\n")
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer)

    def _handle_alive(self):
        pass

    def broadcast(self):
        thread_alive = threading.Timer(10, self._broadcast_alive)
        thread_alive.start()
        thread_alive.join()  # Espera thread_alive terminar
        self.broadcast()

    def _broadcast_alive(self):
        print("Sending ALIVE")
        msg = Message("ALIVE")
        for peer in self.peers:
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer)


if __name__ == "__main__":

    server = Servidor()
    listening_thread = threading.Thread(target=server._receive)
    alive_thread = threading.Thread(target=server.broadcast)

    listening_thread.start()
    alive_thread.start()

    print("SERVER ON ...")

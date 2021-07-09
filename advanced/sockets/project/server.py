import socket
import threading
# running locally
from message import Message

import json


class Servidor:

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 10098
    SERVER = (HOST, PORT)
    BUFFERSIZE = 1024

    def __init__(self):
        self.UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.HOST, self.PORT))
        self.peers = {}  # Python Dict são thread safe

    def _receive(self):

        while True:
            try:
                data, peer_udp = self.UDPServerSocket.recvfrom(self.BUFFERSIZE)
                recv_msg = json.loads(data.decode('utf-8'))  # Transforma json em dict
                # Criar uma thread para cada requisição de um cliente
                thread = threading.Thread(
                    target=self._handle_request, args=(recv_msg,peer_udp))

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

    def _handle_request(self, recv_msg, peer_udp):
        peer = tuple(recv_msg["sender"])  # Peer que fez a requisição
        msg_type = recv_msg["msg_type"]  # Tipo de requisição
        content = recv_msg["content"]  # Conteúdo da requisição

        if msg_type == "JOIN":
            return self._handle_join(peer, peer_udp, content)
            
        elif msg_type == "SEARCH":
            return self._handle_search(peer, peer_udp, content)

        elif msg_type == "LEAVE":
            return self._handle_leave(peer, peer_udp)

        elif msg_type == "ALIVE_OK":
            self._handle_alive()

    def _handle_join(self, peer, peer_udp, content):
        """
        Grava peer na estrutura de dados do servidor somente caso não esteja conectado.
        """
        file_lst = content.strip() # Retira possíveis espaços em branco do começo e final da string
        if peer not in self.peers:
            self.peers[peer] = file_lst.split()  # Grava o peer no servidor
            print(f"Peer [{peer[0]}]:{peer[1]} adicionado com arquivos {file_lst}")
            msg = Message(content=None, msg_type="JOIN_OK", sender=self.SERVER)
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer_udp)
        else:
            msg = Message(content="Você já está conectado\n", msg_type="JOIN_OK", sender=self.SERVER)
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer_udp)
            print(f"Peer [{peer[0]}]:{peer[1]} já está conectado.")

    def _handle_search(self, sender_peer, peer_udp, content):
        """
        Encontra quais peers tem o arquivo solicitado.
        """
        filename = content.strip() # 
        print(f"Peer [{sender_peer[0]}]:[{sender_peer[1]}] solicitou arquivo {filename}")
        print(sender_peer)
        has_peers = [f"{peer[0]}:{peer[1]}" for peer in self.peers if (filename in self.peers[peer]) and (sender_peer != peer)]
        msg = Message(content="[" + " ".join(has_peers) + "]", 
                      msg_type="SEARCH",
                      sender=self.SERVER,
                      extra_info=filename)

        self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer_udp)

    def _handle_leave(self, peer, peer_udp):
        if peer in self.peers:
            self.peers.pop(peer)  # Retira o peer do servidor
            msg = Message(content=None, msg_type="LEAVE_OK", sender=self.SERVER)
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer_udp)

    def _handle_alive(self):
        pass

    def broadcast(self):
        thread_alive = threading.Timer(30, self._broadcast_alive)
        thread_alive.start()
        thread_alive.join()  # Espera thread_alive terminar
        self.broadcast()

    def _broadcast_alive(self):
        print("Sending ALIVE")
        msg = Message(content=None, msg_type="ALIVE", sender=self.SERVER)
        # with futures.ThreadPoolExecutor(max_workers=5) as ex:
        #     results = ex.map(task, range(1, 6), timeout=3)
        for peer in self.peers:
            self.alive_timeout = 0
            self.UDPServerSocket.sendto(msg.to_json("utf-8"), peer)


if __name__ == "__main__":

    server = Servidor()
    listening_thread = threading.Thread(target=server._receive)
    alive_thread = threading.Thread(target=server.broadcast)

    listening_thread.start()
    alive_thread.start()

    print("SERVER ON ...")

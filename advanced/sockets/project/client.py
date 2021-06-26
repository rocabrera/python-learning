import os   # Utilitys do sistema operacional
import sys  # Para pegar folder no qual os dados estão
import glob  # Percorre com regex os files de um folder
import json  # Utilizado para fazer parse da mensagem

import socket
import threading

from message import Message


class Peer:

    SERVER_ADDRESS = "127.0.1.1"
    SERVER_PORT = 10098
    SERVER_ID = (SERVER_ADDRESS, SERVER_PORT)
    BUFFER_SIZE = 1024

    def __init__(self, files_path):
        self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.files_path = files_path
        self.files = " ".join([os.path.basename(file_name)
                              for file_name in files_path])

    def _receive(self):
        while True:
            try:
                data, peer = self.UDPClientSocket.recvfrom(self.BUFFERSIZE)

                recv_msg = json.loads(data.decode('utf-8'))  # Transforma json em dict

                request, msg = recv_msg["message"]
                thread = threading.Thread(target=self._handle_request,
                                          args=(peer, request, msg,))
                thread.start()
                thread.join()

            except Exception:
                pass

    def _handle_request(self, peer, request, msg):
        if request == "ALIVE":
            return self._handle_alive(msg)

    def _handle_alive(self, msg):
        msg = Message("ALIVE_OK\n")
        self.UDPClientSocket.sendto(msg.to_json().encode("utf-8"), peer)

    def _make_request(self):
        while True:
            try:

                request = input("Digite a requisição [JOIN,LEAVE]:")
                thread = threading.Thread(target=self._handle_write, args=(request,))
                thread.start()
                thread.join()

            except SystemExit as e:
                print(e)
                return None

    def _handle_write(self, request):

        if request == "JOIN":
            self.join()
        elif request == "LEAVE":
            self.leave()
            sys.exit("Desconectado")
        else:
            return "Comando Invalido."

    def join(self):
        msg = Message(f"JOIN: {self.files}")
        self.UDPClientSocket.sendto(
            msg.to_json().encode("utf-8"), self.SERVER_ID)
        data, _ = self.UDPClientSocket.recvfrom(self.BUFFER_SIZE)
        recv_msg = json.loads(data.decode('utf-8'))
        print(recv_msg["message"])
        print(
            f"Sou o peer [{self.SERVER_ID[0]}]:{self.SERVER_ID[1]} com arquivos {self.files}")

    def leave(self):
        msg = Message("LEAVE:")
        self.UDPClientSocket.sendto(
            msg.to_json().encode("utf-8"), self.SERVER_ID)
        data, server = self.UDPClientSocket.recvfrom(self.BUFFER_SIZE)
        recv_msg = json.loads(data.decode('utf-8'))
        print(recv_msg["message"])


if __name__ == "__main__":

    # file_folder_path = sys.argv[1]
    file_folder_path = "data/files"
    files_path = [file_name for file_name in glob.glob(
        f"{file_folder_path}/*.txt")]
    peer = Peer(files_path)
    print(peer.files)
    print(peer.files_path)
    peer._make_request()
    print("Ouvindo")
    peer._receive()

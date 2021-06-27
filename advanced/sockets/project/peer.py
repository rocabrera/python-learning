import os   # Utilitys do sistema operacional
import sys  # Para pegar folder no qual os dados estão
import glob  # Percorre com regex os files de um folder
import json  # Utilizado para fazer parse da mensagem

import socket
import threading

from message import Message


class Peer:

    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 10510

    SERVER_ADDRESS = "127.0.1.1"
    SERVER_PORT = 10098
    SERVER = (SERVER_ADDRESS, SERVER_PORT)
    BUFFERSIZE = 1024

    def __init__(self, files_path):
        self.UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Preciso fazer bind aqui?
        # self.UDPClientSocket.bind((self.HOST, self.PORT))
        self.files_path = files_path
        self.files = " ".join([os.path.basename(file_name)
                              for file_name in files_path])

    def _receive(self):
        while True:
            data, server = self.UDPClientSocket.recvfrom(self.BUFFERSIZE)

            recv_msg = json.loads(data.decode('utf-8'))  # Transforma json em dict
            thread = threading.Thread(target=self._handle_request, args=(server, recv_msg))
            thread.start()
            thread.join()

    def _handle_request(self, server, recv_msg):

        request = recv_msg["message"].strip("\n")

        if request == "JOIN_OK":
            self._handle_join()

        elif request == "LEAVE_OK":
            self._handle_leave()  # No futuro preciso desligar o client aqui

        elif request == "ALIVE":
            return self._handle_alive()

    def _handle_join(self):
        print(f"Sou o peer [{self.HOST}]:{self.PORT} com arquivos {self.files}")

    def _handle_leave(self):
        sys.exit("Desconectado")

    def _handle_alive(self):
        print("ESTOU VIVO - TESTE")
        msg = Message("ALIVE_OK:\n")
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def _request(self):
        while True:
            request = input("Digite a requisição [JOIN,LEAVE]:")
            thread = threading.Thread(target=self._handle_write, args=(request,))
            thread.start()
            thread.join()

    def _handle_write(self, request):

        if request == "JOIN":
            self.join()
        elif request == "LEAVE":
            self.leave()
        else:
            return "Comando Invalido."

    def join(self):
        msg = Message(f"JOIN: {self.files}")
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def leave(self):
        msg = Message("LEAVE:")
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)


if __name__ == "__main__":

    # file_folder_path = sys.argv[1]
    file_folder_path = "data/files"
    files_path = [file_name for file_name in glob.glob(f"{file_folder_path}/*.txt")]

    peer = Peer(files_path)
    print("ONLINE\n")
    listening_thread = threading.Thread(target=peer._receive)
    alive_thread = threading.Thread(target=peer._request)

    listening_thread.start()
    alive_thread.start()

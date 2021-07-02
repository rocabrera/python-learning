import os   # Utilitys do sistema operacional
import sys  # Para pegar folder no qual os dados estão
import glob  # Percorre com regex os files de um folder
import json  # Utilizado para fazer parse da mensagem
import time
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
        self.menu_str = "Digite a requisição [JOIN, SEARCH, LEAVE]:" 

    def _receive(self):
        while True:
            data, server = self.UDPClientSocket.recvfrom(self.BUFFERSIZE)

            recv_msg = json.loads(data.decode('utf-8'))  # Transforma json em dict
            thread = threading.Thread(target=self._handle_request, args=(server, recv_msg))
            thread.start()
            thread.join()

    def _handle_request(self, server, recv_msg):

        text_msg = recv_msg["message"].strip("\n")

        if recv_msg["type_msg"] == "OK":

            if text_msg == "JOIN_OK":
                self._handle_join()

            elif text_msg == "LEAVE_OK":
                self._handle_leave()  # No futuro preciso desligar o client aqui

            elif text_msg == "ALIVE":
                return self._handle_alive()

        elif recv_msg["type_msg"] == "SEARCH":

            self._handle_search(text_msg)

    def _handle_join(self):
        print(f"Sou o peer [{self.HOST}]:{self.PORT} com arquivos {self.files}\n")

    def _handle_search(self, msg):
        print(f"Peers com arquivo solicitado: {msg}")

    def _handle_leave(self):
        sys.exit("Desconectado")

    def _handle_alive(self):        
        msg = Message("ALIVE_OK:\n", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def _request(self):
        while True:
            time.sleep(0.1)
            request = input(self.menu_str)
            thread = threading.Thread(target=self._handle_write, args=(request,))
            thread.start()
            thread.join()

    def _handle_write(self, request):

        if request.upper() == "JOIN":
            self.join()

        elif request.upper() == "LEAVE":
            self.leave()

        elif request.upper() == "SEARCH":
            requested_file = input("Digite o nome do arquivo buscado:")
            self.search(requested_file)

        else:
            print("Comando Invalido.")

    def search(self, requested_file):
        msg = Message(f"SEARCH: {requested_file}", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def join(self):
        msg = Message(f"JOIN: {self.files}", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)

    def leave(self):
        msg = Message("LEAVE:", None)
        self.UDPClientSocket.sendto(msg.to_json("utf-8"), self.SERVER)


if __name__ == "__main__":

    # file_folder_path = sys.argv[1]
    file_folder_path = "data/peer1"
    files_path = [file_name for file_name in glob.glob(f"{file_folder_path}/*.txt")]

    peer = Peer(files_path)
    print("ONLINE\n")
    listening_thread = threading.Thread(target=peer._receive)
    alive_thread = threading.Thread(target=peer._request)

    listening_thread.start()
    alive_thread.start()
